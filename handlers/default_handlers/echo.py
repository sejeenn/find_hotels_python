from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(func=lambda message: True)
def bot_echo(message: Message):
    if message.text == 'привет':
        bot.reply_to(message, 'Реагируем на слово "привет"')
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                              f"{message.text}")
