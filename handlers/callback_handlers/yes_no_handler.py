from loader import bot
from telebot import types
from telebot.types import Message
from telebot.callback_data import CallbackData
# from telebot.custom_filters import TextFilter, TextMatchFilter, IsReplyFilter


@bot.inline_handler(lambda call: call.query == 'yes')
def yes_no(call):
    print(call.data)
