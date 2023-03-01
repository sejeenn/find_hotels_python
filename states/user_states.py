from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    command = State()
    input_city = State()
    destinationId = State()
    quantity_hotels = State()
    photo_need = State()
    photo_count = State()
    pageSize = State()
    input_date = State()
    checkIn = State()
    checkOut = State()
    priceMin = State()
    priceMax = State()
    sortOrder = State()
    landmarkIn = State()
    landmarkOut = State()
