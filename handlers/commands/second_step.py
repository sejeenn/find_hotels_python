from loader import bot
from telebot.types import Message
from loguru import logger
from states.user_inputs import UserInputState


def continue_input(message: Message):
    logger.info('Перешли ко второму этапу ввода данных')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['command'] == '/lowprice':
            data['sort_order'] = 'PRICE'
        elif data['command'] == '/hiprice':
            data['sort_order'] = 'PRICE_HIGHEST_FIRST'
        # data['city'] = city
        # data['destination_id'] = destination_id
    bot.set_state(message.from_user.id, UserInputState.pageNumber, message.chat.id)
    bot.send_message(message.from_user.id, 'Сколько страниц вывести?')


@bot.message_handler(state=UserInputState.pageNumber)
def input_page_number(message: Message) -> None:
    logger.info('Ввод количества страниц')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['page_number'] = message.text
    bot.set_state(message.from_user.id, UserInputState.pageSize, message.chat.id)
    bot.send_message(message.from_user.id, 'Сколько отелей на странице вывести?')


@bot.message_handler(state=UserInputState.pageSize)
def input_page_size(message: Message) -> None:
    logger.info('Ввод количества отелей на странице')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['page_size'] = message.text
    bot.set_state(message.from_user.id, UserInputState.priceMin, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите минимальную стоимость номера')


@bot.message_handler(state=UserInputState.priceMin)
def input_price_min(message: Message) -> None:
    logger.info('Ввод минимальной стоимости номера')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_min'] = message.text
    bot.set_state(message.from_user.id, UserInputState.priceMax, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите максимальную стоимость номера')


@bot.message_handler(state=UserInputState.priceMax)
def input_price_max(message: Message) -> None:
    logger.info('Ввод максимальной стоимости номера')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price_max'] = message.text
    bot.set_state(message.from_user.id, UserInputState.checkIn, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи дату заезда')


@bot.message_handler(state=UserInputState.checkIn)
def input_checkin(message: Message) -> None:
    logger.info('Ввод даты заезда')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in'] = message.text     # ???????????
    bot.set_state(message.from_user.id, UserInputState.checkOut, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи дату выезда')


@bot.message_handler(state=UserInputState.checkOut)
def input_checkin(message: Message) -> None:
    logger.info('Ввод даты заезда')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_out'] = message.text     # ???????????
    bot.send_message(message.from_user.id, f"Введенные данные:"
                                           f"\nКоманда: {data['command']}"
                                           f"\nВведенный город: {data['input_city']}"
                                           f"\nDestination ID: {data['destination_id']}"
                                           f"\nЧисло страниц: {data['page_number']}"
                                           f"\nЧисло отелей на странице: {data['page_size']}"
                                           f"\nМинимальная стоимость номера: {data['price_min']}"
                                           f"\nМаксимальная стоимость номера: {data['price_max']}"
                                           f"\nСортировка: {data['sort_order']}")
