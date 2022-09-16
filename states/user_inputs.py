from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    input_city = State()
    destination_id = State()
