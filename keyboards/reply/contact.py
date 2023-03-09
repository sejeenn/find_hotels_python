from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    """
    Возможность отправить свои контактные данные
    : return keyboard : Возвращает кнопку ответа
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))
    return keyboard
