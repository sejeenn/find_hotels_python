from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import database
from keyboards.inline.history_buttons import get_history_queries


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    logger.info('Выбрана команда history!')
    records = database.read_from_db.read_query()
    logger.info(f'Получены записи из таблицы query:\n {records}')
    # get_history_queries(message, records)
    bot.send_message(message.chat.id, "Введи номер нужного запроса:")
    for item in records:
        bot.send_message(message.chat.id, f"({item[0]}). Дата и время: {item[1]}. Город: {item[2]}")
    mesg = bot.send_message(message.chat.id, "Введи номер нужного запроса:")
    bot.register_next_step_handler(mesg, show_history)


def show_history(message):
    history_dict = database.read_from_db.get_history_response(message.text)
    for hotel in history_dict.items():
        medias = []
        caption = f"Название отеля: {hotel[1]['name']}]\n Адрес отеля: {hotel[1]['address']}\nСтоимость проживания в " \
                  f"сутки: {hotel[1]['price']}\nРасстояние до центра: {hotel[1]['distance']}"
        urls = hotel[1]['images']
        for number, url in enumerate(urls):
            if number == 0:
                medias.append(InputMediaPhoto(media=url, caption=caption))
            else:
                medias.append(InputMediaPhoto(media=url))
        bot.send_media_group(message.chat.id, medias)
