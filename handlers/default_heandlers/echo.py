from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    if message.text == 'привет':
        bot.reply_to(message, 'Я приветствую тебя дорогой друг!')
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                              f"{message.text}")
