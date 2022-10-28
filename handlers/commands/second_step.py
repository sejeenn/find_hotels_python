from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import datetime
from states.user_inputs import UserInputState
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from keyboards.calendar import main_calendar
from utils.find_hotels import get_dict_hotels

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
        else:
            data['sort_order'] = 'best_deal'

    bot.set_state(message.from_user.id, UserInputState.pageSize, message.chat.id)
    bot.send_message(message.from_user.id, 'Сколько отелей на странице вывести? Максимум 25')


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

    main_calendar.calendar_date(message, 'Выберите дату заезда:')

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
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_end:
                if 'check_in' in data_end:
                    checkin = int(''.join(data_end['check_in'].split('-')))
                    if select_date > checkin:
                        bot.send_message(message.from_user.id, 'Записал дату выезда:')
                        data_end['check_out'] = date.strftime('%Y-%m-%d')
                        end_input(message, data_end)
                    else:
                        bot.send_message(message.from_user.id, 'Дата выезда должна быть больше '
                                                               'даты заезда, введи еще раз!')
                        main_calendar.calendar_date(message, 'Выберите дату выезда')
                else:
                    if select_date >= now_date:
                        data_end['check_in'] = date.strftime('%Y-%m-%d')
                        bot.send_message(message.from_user.id, 'Записал дату заезда:')
                        main_calendar.calendar_date(message, 'Выберите дату выезда')
                    else:
                        bot.send_message(message.from_user.id, 'Дата заезда должна быть больше '
                                                               'или равна сегодняшней дате, введи еще раз!')
                        main_calendar.calendar_date(message, 'Выберите дату заезда')

        elif action == "CANCEL":
            bot.send_message(chat_id=call.from_user.id, text="Cancellation",
                             reply_markup=ReplyKeyboardRemove())


def end_input(message, data):
    bot.send_message(message.from_user.id, f"Проверьте правильность ввода данных:"
                                               f"\nКоманда: {data['command']}"
                                               f"\nИщем город: {data['input_city']}"
                                               f"\nDestination_ID: {data['destination_id']}"
                                               f"\nСортировка: {data['sort_order']}"
                                               f"\nЧисло отелей на странице: {data['page_size']}"
                                               f"\nМинимальная стоимость номера: {data['price_min']}"
                                               f"\nМаксимальная стоимость номера: {data['price_max']}"
                                               f"\nДата заезда: {data['check_in']}"
                                               f"\nДата выезда: {data['check_out']}"
                                               f"\n\nВыполняю поиск по заданным параметрам")
    #     Из полученных данных создаем query_string и отправляем ее в поиск.
    querystring = {"destinationId": data['destination_id'],
                   "pageNumber": "1", "pageSize": data['page_size'],
                   "checkIn": data['check_in'], "checkOut": data['check_out'], "adults1": "1",
                   "priceMin": data['price_min'], "priceMax": data['price_max'],
                   "sortOrder": data['sort_order'], "locale": "en_US", "currency": "USD"}

    found_hotels = get_dict_hotels(querystring)
    for key, value in found_hotels.items():
        bot.send_photo(message.from_user.id, value[4])
        bot.send_message(message.from_user.id, f"Название отеля: {value[0]}"
                                               f"\nАдрес: {value[1]}"
                                               f"\nСтоимость проживания: {value[2]}"
                                               f"\nРасстояние до {value[3][0]['label']} - {value[3][0]['distance']}"
                                               f"\nРасстояние до {value[3][1]['label']} - {value[3][1]['distance']}")

