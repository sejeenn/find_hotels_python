from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message, Dict


def show_buttons_photo_need_yes_no(message: Message) -> None:
    """
    Вызов в чат инлайн-кнопок с вопросом - нужны ли пользователю фотографии?
    : param message : Message
    : return : None
    """
    logger.info(f'Вывод кнопок о необходимости фотографий пользователю. User_id: {message.chat.id}')
    keyboard_yes_no = types.InlineKeyboardMarkup()
    keyboard_yes_no.add(types.InlineKeyboardButton(text='ДА', callback_data='yes'))
    keyboard_yes_no.add(types.InlineKeyboardButton(text='НЕТ', callback_data='no'))
    bot.send_message(message.chat.id, "Нужно вывести фотографии?", reply_markup=keyboard_yes_no)


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    """
    Функция, из словаря возможных городов, формирует инлайн-клавиатуру с вариантами городов, и посылает её в чат.
   : param message : Message
    : param possible_cities : Dict словарь, с возможными вариантами городов
    : return : None
    """
    logger.info(f'Вывод кнопок с вариантами городов пользователю. User_id: {message.chat.id}')
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)

