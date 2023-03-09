from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: True)
def bot_echo(message: Message) -> None:
    if message.text == 'привет':
        bot.reply_to(message, f'Реагируем на слово "привет", И вам {message.from_user.full_name} - привет!')
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                              f"{message.text}")
