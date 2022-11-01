from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
from utils.find_hotels import get_dict_hotels
from utils.find_hotels_photo import get_photo
from states.user_inputs import UserInputState


def finish_him(message: Message, data) -> None:
    """"""
    logger.info('Завершаем все наши вводы, выдаем сообщение о том что ввел пользователь и '
                'после чего посылаем пользователю найденные отели, либо сообщение что отели не найдены.')
    if data['command'] == '/lowprice':
        data['sort_order'] = 'PRICE'
    elif data['command'] == '/hiprice':
        data['sort_order'] = 'PRICE_HIGHEST_FIRST'
    elif data['command'] == '/bestdeal':
        data['sort_order'] = 'DISTANCE_FROM_LANDMARK'
    bot.send_message(message.from_user.id, f"Выполняю поиск по следующим критериям:"
                                           f"\n\nКоманда: {data['command']}"
                                           f"\nИщем город: {data['input_city']}"
                                           f"\nDestination_ID: {data['destination_id']}"
                                           f"\nСортировка: {data['sort_order']}"
                                           f"\nЧисло отелей на странице: {data['page_size']}"
                                           f"\nМинимальная стоимость номера: {data['price_min']}"
                                           f"\nМаксимальная стоимость номера: {data['price_max']}"
                                           f"\nНужны ли фотографии? {data['photo_need']}"
                                           f"\nКоличество фотографий: {data['photo_count']}"
                                           f"\nДата заезда: {data['check_in']}"
                                           f"\nДата выезда: {data['check_out']}")
    #     Из полученных данных создаем query_string и отправляем ее в поиск.
    querystring = {"destinationId": data['destination_id'],
                   "pageNumber": "1", "pageSize": data['page_size'],
                   "checkIn": data['check_in'], "checkOut": data['check_out'], "adults1": "1",
                   "priceMin": data['price_min'], "priceMax": data['price_max'],
                   "sortOrder": data['sort_order'], "locale": "en_US", "currency": "USD"}
    if data['command'] == '/bestdeal':
        bot.set_state(message.from_user.id, UserInputState.landmarkIn, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите начало диапазона "расстояние до центра от 0.1":')

    elif data['command'] == '/lowprice' or '/hiprice':
        found_hotels = get_dict_hotels(querystring)
        print(found_hotels)
        if found_hotels:
            print_found_hotels(message, found_hotels)


def header(message: Message, value):
    bot.send_message(message.from_user.id, f"Название отеля: {value[0]}"
                                           f"\nID: {value[5]}"
                                           f"\nАдрес: {value[1]}"
                                           f"\nСтоимость проживания: {value[2]}"
                                           f"\nРасстояние до {value[3][0]['label']} - {value[3][0]['distance']}"
                                           f"\nРасстояние до {value[3][1]['label']} - {value[3][1]['distance']}")


@bot.message_handler(state=UserInputState.landmarkIn)
def input_landmark_in(message: Message) -> None:
    """

            :param message:
            Записываем начальный диапазон расстояния до центра
        """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["landmark_in"] = message.text
    bot.set_state(message.from_user.id, UserInputState.landmarkOut, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите конец диапазона "расстояние до центра":')


@bot.message_handler(state=UserInputState.landmarkOut)
def input_landmark_out(message: Message) -> None:
    """

        :param message:
        Записываем конечный диапазон расстояния до центра и формируем словарь для поиска отелей, который
        отправим серверу hotels.com в ответ возвращается словарь с найденными отелями, либо сообщение,
        что отели с такими данными в данном городе не найдены.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["landmark_out"] = message.text
    querystring = {"destinationId": data['destination_id'], "pageNumber": "1", "pageSize": data['page_size'],
                   "checkIn": data['check_in'], "checkOut": data['check_out'], "adults1": "1",
                   "priceMin": data['price_min'], "priceMax": data['price_max'], "sortOrder": data['sort_order'],
                   "locale": "en_US", "currency": "USD",
                   'landmarkIds': f"{data['landmark_in']}, {data['landmark_out']}"}
    found_hotels = get_dict_hotels(querystring)
    if len(found_hotels) > 0:
        print_found_hotels(message, found_hotels)
    else:
        bot.send_message(message.from_user.id, 'Извините, но по заданным параметрам не найдено ни одного отеля.'
                                               'Попробуйте изменить параметры поиска и сделать запрос ещё раз.')


def print_found_hotels(message: Message, found_hotels):
    """
        :param message
        :param found_hotels - словарь с найденными отелями

        Получив словарь с найденными отелями и отсортированными по заданным параметрам выдаем результаты
        поиска пользователю в чат. Если счетчик data['photo_count']
        больше нуля, мы понимаем что пользователю нужны фотографии и делаем запрос на поиск фотографий
        для каждого отеля. Фотографии выводим общим блоком - альбомом.
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
