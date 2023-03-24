from loader import bot
from telebot import types
from telebot.types import Message, List


def get_history_queries(message: Message, records: list) -> None:
    """
    Из списка поисковых запросов, взятых из БД формируем inline клавиатуру,
    чтобы пользователь мог выбрать нужную ему дату и город из истории поиска.
   : param message : Message
    : param records : lict записи из базы данных о том что искал пользователь
    : return : None
    """
    keyboards_queries = types.InlineKeyboardMarkup()
    for item in records:
        caption = f"Дата запроса: {item[1]}, Введен город: {item[2]}"
        keyboards_queries.add(types.InlineKeyboardButton(text=caption, callback_data=item[1]))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите интересующий вас запрос",
                     reply_markup=keyboards_queries)

