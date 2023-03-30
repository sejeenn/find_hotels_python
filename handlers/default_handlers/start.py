from telebot.types import Message
import database
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    database.add_to_bd.add_user(message)
