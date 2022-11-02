from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
from utils.find_hotels import get_dict_hotels
from utils.find_hotels_photo import get_photo
from states.user_inputs import UserInputState


def finish_him(message: Message, data) -> None:
    """
    :param message:
    :param data - словарь в котором собраны все данные что пользователь ввёл
        Исходя из того какая команда выбрана пользователем в начале сбора информации, выбираем,
        по какому критерию будет сортироваться сервером информация.
    """
    logger.info('Завершаем все наши вводы, выдаем сообщение о том что ввел пользователь и '
                'после чего посылаем пользователю найденные отели, либо сообщение что отели не найдены.')
    if data['command'] == '/bestdeal':
        data['sort_order'] = 'DISTANCE_FROM_LANDMARK'
        bot.set_state(message.from_user.id, UserInputState.landmark_lds_In, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите начало диапазона "расстояние до центра (в милях).'
                                               '\nМинимальное значение 0":')
    else:
        if data['command'] == '/lowprice':
            data['sort_order'] = 'PRICE'
        elif data['command'] == '/hiprice':
            data['sort_order'] = 'PRICE_HIGHEST_FIRST'
        # отправляем пользователю данные которые он ввел и начинаем поиск
        send_entered_data(message, data)
        # Из полученных данных создаем query_string и отправляем ее в поиск.
        querystring = {"destinationId": data['destination_id'],
                       "pageNumber": "1", "pageSize": data['page_size'],
                       "checkIn": data['check_in'], "checkOut": data['check_out'], "adults1": "1",
                       "priceMin": data['price_min'], "priceMax": data['price_max'],
                       "sortOrder": data['sort_order'], "locale": "en_US", "currency": "USD"}
        found_hotels = get_dict_hotels(querystring)
        # Если полученный словарь больше нуля, выводим в чат найденные отели
        if len(found_hotels) > 0:
            send_found_hotels(message, found_hotels)
        else:
            bot.send_message(message.from_user.id, 'К сожалению, по заданным параметрам отелей не найдено.'
                                                   '\nПопробуйте изменить параметры поиска.')


@bot.message_handler(state=UserInputState.landmark_lds_In)
def input_landmark_in(message: Message) -> None:
    """
        :param: message
        Ввод начала диапазона расстояния до центра, минимальное число от 0
    """
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["landmark_in"] = message.text
        bot.set_state(message.from_user.id, UserInputState.landmark_lds_Out, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите конец диапазона "расстояние до центра в милях, '
                                               'больше начала диапазона":')
    else:
        bot.send_message(message.from_user.id, 'Начало диапазона должно быть числом! Повторите ввод!')


@bot.message_handler(state=UserInputState.landmark_lds_Out)
def input_landmark_out(message: Message) -> None:
    """
        :param: message
        Ввод конца диапазона расстояния до центра. Это должно быть число, не менее числа чем начало
        диапазона
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            if int(message.text) > int(data['landmark_in']):
                data["landmark_out"] = message.text
                diapasons = data['landmark_in'] + ', ' + data['landmark_out']
                # отправляем пользователю данные которые он ввел и начинаем поиск
                send_entered_data(message, data)
                querystring = {"destinationId": data['destination_id'], "pageNumber": "1",
                               "pageSize": data['page_size'],
                               "checkIn": data['check_in'], "checkOut": data['check_out'], "adults1": "1",
                               "priceMin": data['price_min'], "priceMax": data['price_max'],
                               "sortOrder": data['sort_order'],
                               "locale": "en_US", "currency": "USD",
                               "landmarkIds": diapasons}
                found_hotels = get_dict_hotels(querystring)
                send_found_hotels(message, found_hotels)
            else:
                bot.send_message(message.from_user.id, 'Конец диапазона не может быть больше начала. Повтори ввод!')
        except ValueError:
            bot.send_message(message.from_user.id, 'Ввод должен состоять из цифр!')


def send_found_hotels(message: Message, found_hotels):
    """
        :param: message
        :param: Dict found_hotels - словарь с информацией об найденных отелях
        Выдача в чат результатов поиска, если счетчик фотографий больше нуля, то следовательно,
        пользователю нужны фотографии и бот отправляет дополнительный запрос к серверу, отдельно для
        каждого отеля. Где получает ссылки на фотографии отеля. Которые компонуются в альбом и выдаются
        в чат, пользователю.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if int(data['photo_count']) > 0:
            logger.info('Нужно вывести дополнительные фотографии, переходим к их поиску')
        bot.send_message(message.from_user.id, 'Найдены следующие отели:')
        for key, value in found_hotels.items():
            if int(data['photo_count']) > 0:
                photos = get_photo(value[5], int(data['photo_count']))
                medias = []
                for link in photos:
                    medias.append(InputMediaPhoto(link))
                bot.send_media_group(message.from_user.id, medias)
                header(message, value)
            else:
                header(message, value)


def header(message: Message, value):
    """
    :param: message
    :param: value словарь с информация об одном конкретном отеле, которая формируется в блок
    и выдается в чат пользователю
    """
    bot.send_message(message.from_user.id, f"Название отеля: {value[0]}"
                                           f"\nID: {value[5]}"
                                           f"\nАдрес: {value[1]}"
                                           f"\nСтоимость проживания: {value[2]}"
                                           f"\nРасстояние до {value[3][0]['label']} - {value[3][0]['distance']}"
                                           f"\nРасстояние до {value[3][1]['label']} - {value[3][1]['distance']}")


def send_entered_data(message: Message, data):
    """
    Сообщение пользователю, о той информации по которой будет осуществляться поиск (то что он ввёл)
    """
    text_message = f"Выполняю поиск по следующим критериям: \n\nКоманда: {data['command']}\nИщем город: " \
                   f"{data['input_city']}\nDestination_ID: {data['destination_id']}\nСортировка: " \
                   f"{data['sort_order']}\nЧисло отелей на странице: {data['page_size']}\nМинимальная " \
                   f"стоимость номера: {data['price_min']}\nМаксимальная стоимость номера: " \
                   f"{data['price_max']}\nНужны ли фотографии? {data['photo_need']}\nКоличество фотографий: " \
                   f"{data['photo_count']}\nДата заезда: {data['check_in']}\nДата выезда: " \
                   f"{data['check_out']}"
    if 'landmark_in' and 'landmark_out' in data:
        text_message = text_message + f"\nНачало диапазона: {data['landmark_in']}" \
                                      f"\nКонец диапазона: {data['landmark_out']}"
    bot.send_message(message.from_user.id, text_message)

