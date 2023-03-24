from loader import bot
from telebot.types import CallbackQuery
from loguru import logger


@bot.callback_query_handler(func=lambda call: True)
def query_callback(call: CallbackQuery) -> None:
    print(call.data)
    bot.send_message(call.message.chat.id, 'Как хорошо что ты пришел')
