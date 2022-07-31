from loader import bot
from telebot.types import Message
from handlers.custom_handlers.get_destination_id import find_city


@bot.message_handler(commands=['lowprice'])
def survey(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Привет {message.from_user.username}, Введи город в котором нужно найти "
                                           f"отель")
    bot.register_next_step_handler(message.text, buttons=find_city(message))
