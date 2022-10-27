from loader import bot
from telebot.types import Message
import datetime
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


def my_calendar(message: Message):
    now = datetime.datetime.now()  # Получение текущей даты
    bot.send_message(message.from_user.id, "Выбери нужную дату:", reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,
        ),
    )
