from loader import bot
from telebot.types import Message
from loguru import logger
import datetime
from states.user_inputs import UserInputState
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from keyboards.calendar import main_calendar

calendar = Calendar(language=RUSSIAN_LANGUAGE)
from telebot.types import ReplyKeyboardRemove, CallbackQuery

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

    # -----------Пытаемся освоить ввод даты заезда-выезда-----------------------

    main_calendar.calendar_date(message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
    def check_in(call):
        name, action, year, month, day = call.data.split(calendar_1_callback.sep)
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
        if action == "DAY":
            bot.send_message(chat_id=call.from_user.id, text=f"{date.strftime('%Y-%m-%d')}",
                             reply_markup=ReplyKeyboardRemove())
            now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
            select_date = int(date.strftime('%Y%m%d'))
            bot.set_state(message.from_user.id, UserInputState.checkIn, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_1:
                if 'check_in' not in data_1:
                    data_1['check_in'] = date.strftime('%Y-%m-%d')
                    bot.send_message(message.from_user.id, f"Дата заезда записана: {data_1['check_in']}")
                    logger.info(data_1['check_in'])
                else:
                    data_1['check_out'] = date.strftime('%Y-%m-%d')
                    bot.send_message(message.from_user.id, f"Дата выезда записана: {data_1['check_out']}")
                    logger.info(data_1['check_out'])
                    end_input(message)
                if 'check_out' not in data_1:
                    main_calendar.calendar_date(message)
        elif action == "CANCEL":
            bot.send_message(chat_id=call.from_user.id, text="Cancellation",
                             reply_markup=ReplyKeyboardRemove())


def end_input(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data)
        bot.send_message(message.from_user.id, f"Проверьте правильность ввода данных:"
                                               f"\nКоманда: {data['command']}"
                                               f"\nИщем город: {data['input_city']}"
                                               f"\nDestination_ID: {data['destination_id']}"
                                               f"\nСортировка: {data['sort_order']}"
                                               f"\nЧисло страниц: {data['page_number']}"
                                               f"\nЧисло отелей на странице: {data['page_size']}"
                                               f"\nМинимальная стоимость номера: {data['price_min']}"
                                               f"\nМаксимальная стоимость номера: {data['price_max']}"
                                               f"\nДата заезда: {data['check_in']}"
                                               f"\nДата выезда: {data['check_out']}"
                                               f"\nЕсли всё верно, нажми на кнопку, получишь результат! "
                                               f"\nИли повтори ввод!")
