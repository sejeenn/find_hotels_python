from loader import bot
from telebot import types
from telebot.types import Message
from telebot.callback_data import CallbackData


def yes_no(message: Message):
    keyboard_yes_no = types.ReplyKeyboardMarkup(row_width=2)
    key_yes = types.KeyboardButton('yes')
    key_no = types.KeyboardButton('no')
    keyboard_yes_no.add(key_yes, key_no)
    bot.send_message(message.from_user.id, "Нужны ли вам фотографии?", reply_markup=keyboard_yes_no)
