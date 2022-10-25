from loader import bot
from telebot import types


def buttons_gen(message, possible_cities):
    """
        Данный модуль принимает сообщение в котором содержится словарь с
        возможными вариантами городов и формирует динамический блок кнопок.
        Которые будут выданы в чат.

    """
    # вывод возможных городов по запросу "rome" (Рим) step_1_rome.json
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)
