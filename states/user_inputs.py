from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    command = State()
    input_city = State()
    destinationId = State()
    pageNumber = State()
    pageSize = State()
    checkIn = State()
    checkOut = State()
    priceMin = State()
    priceMax = State()
    sortOrder = State()
