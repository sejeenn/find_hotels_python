from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    class UserInfoState
    запоминает состояния пользователя

    """
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()
