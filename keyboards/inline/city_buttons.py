from loader import bot
from telebot import types
from telebot.types import Message, Dict


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    """
    Функция, из словаря возможных городов, формирует инлайн-клавиатуру с вариантами городов, и посылает её в чат.
   : param message : Message
    : param possible_cities : Dict словарь, с возможными вариантами городов
    : return : None
    """
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)
