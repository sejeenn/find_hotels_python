from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
from utils.find_hotels import get_dict_hotels
from utils.find_hotels_photo import get_photo


def finish_him(message: Message, data) -> None:
    logger.info('Завершаем все наши вводы, выдаем сообщение о том что ввел пользователь и '
                'после чего посылаем пользователю найденные отели, либо сообщение что отели не найдены.')
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
    found_hotels = get_dict_hotels(querystring)
    if int(data['photo_count']) > 0:
        logger.info('Нужно вывести дополнительные фотографии, переходим к их поиску')

    if found_hotels:
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
    bot.send_message(message.from_user.id, f"Название отеля: {value[0]}"
                                           f"\nID: {value[5]}"
                                           f"\nАдрес: {value[1]}"
                                           f"\nСтоимость проживания: {value[2]}"
                                           f"\nРасстояние до {value[3][0]['label']} - {value[3][0]['distance']}"
                                           f"\nРасстояние до {value[3][1]['label']} - {value[3][1]['distance']}")