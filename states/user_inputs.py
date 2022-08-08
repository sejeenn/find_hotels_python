from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    input_city = State()
    press_button_city = State()
