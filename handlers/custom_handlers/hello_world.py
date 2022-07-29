from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['hello_world'])
def bot_start(message: Message):
    bot.reply_to(message, f"Обработчик нашей команды 'hello_world'")

