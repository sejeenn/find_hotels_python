from loader import bot
from telebot import types
from telebot.types import Message, Dict


def buttons_gen(message: Message, possible_cities: Dict) -> None:
    """
        Данный модуль принимает сообщение в котором содержится словарь с
        возможными вариантами городов и формирует блок кнопок.
        Которые будут выданы в чат.
        :param message: Сообщение от пользователя.
        :param possible_cities:
    """
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)
