from loader import bot
from telebot.types import Message
from loguru import logger
from states.user_inputs import UserInputState
import datetime
from telebot.types import ReplyKeyboardRemove, CallbackQuery
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


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
    # вызов клавиатуры календаря
    calendar_1(message)


@bot.message_handler(state=UserInputState.checkIn)
def input_checkin(message: Message) -> None:
    logger.info('Ввод даты заезда')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in'] = message.text     # ???????????
    bot.set_state(message.from_user.id, UserInputState.checkOut, message.chat.id)
    # вызов клавиатуры календаря
    calendar_1(message)


@bot.message_handler(state=UserInputState.checkOut)
def input_checkin(message: Message) -> None:
    logger.info('Ввод даты выезда')
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
                                           f"\nСортировка: {data['sort_order']}"
                                           f"\nДата заезда: {data['check_in']}"
                                           f"\nДата выезда: {data['check_out']}")


def calendar_1(message: Message):
    now = datetime.datetime.now()  # Получение текущей даты
    bot.send_message(message.from_user.id, "Выбор даты", reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_inline(call):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"You have chosen {date.strftime('%Y-%m-%d')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Day: {date.strftime('%Y-%m-%d')}")
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Cancellation")
