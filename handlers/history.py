from loader import bot
from telebot.types import Message, Dict
from loguru import logger


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.send_message(message.chat.id, "Тут я покажу что ты искал!")
