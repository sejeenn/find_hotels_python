from loader import bot
from telebot.types import Message
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
import datetime


def calendar_date(message: Message, text):
    now = datetime.datetime.now()  # Получение текущей даты
    bot.send_message(message.from_user.id, text, reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,
        ),
    )