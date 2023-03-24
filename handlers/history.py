from loader import bot
from telebot.types import Message
from loguru import logger
import database
from keyboards.inline.history_queries import get_history_queries

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
        print(hotel)
        bot.send_message(message.chat.id, f"Название отеля: {hotel[1]['name']}]\n"
                                          f"Адрес отеля: {hotel[1]['address']}\n"
                                          f"Стоимость проживания в сутки: {hotel[1]['price']}\n"
                                          f"Расстояние до центра: {hotel[1]['distance']}")
