from loader import bot
from loguru import logger
import datetime
from states.user_states import UserInputState
from keyboards.calendar.telebot_calendar import CallbackData, Calendar
import handlers.input_data
from telebot.types import CallbackQuery
from utils.print_data import print_data


calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:
    """
    Пользователь нажал какую то кнопку на календаре. Если это кнопка какого-то определенного
    дня, то сравниваем эту дату с сегодняшним днём. Дата заезда должна быть либо сегодня, либо
    любой последующий день. А дата выезда не может быть меньше, либо равна, дате заезда.
    : param call : CallbackQuery нажатие на кнопку получения даты в календаре.
    : return : None
    """
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        logger.info('Выбрана какая-то дата, нужно ее проверить. ')
        month = check_month_day(month)
        day = check_month_day(day)
        select_date = year + month + day

        now_year, now_month, now_day = datetime.datetime.now().strftime('%Y.%m.%d').split('.')
        now = now_year + now_month + now_day

        bot.set_state(call.message.chat.id, UserInputState.input_date)
        with bot.retrieve_data(call.message.chat.id) as data:
            if 'checkInDate' in data:
                checkin = int(data['checkInDate']['year'] + data['checkInDate']['month'] + data['checkInDate']['day'])
                if int(select_date) > checkin:
                    logger.info('Ввод и сохранение даты выезда.')
                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}
                    # далее две переменные-заглушки, чтобы не было ошибки при получении словаря с отелями
                    data['landmark_in'] = 0
                    data['landmark_out'] = 0
                    if data['sort'] == 'DISTANCE':
                        bot.set_state(call.message.chat.id, UserInputState.landmarkIn)
                        bot.send_message(call.message.chat.id, 'Введите начало диапазона расстояния от центра '
                                                               '(от 0 миль).')
                    else:
                        print_data(call.message, data)
                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда должна быть больше даты заезда! '
                                                           'Повторите выбор даты!')
                    handlers.input_data.my_calendar(call.message, 'выезда')
            else:
                if int(select_date) >= int(now):
                    logger.info('Ввод и сохранение даты заезда.')
                    data['checkInDate'] = {'day': day, 'month': month, 'year': year}
                    handlers.input_data.my_calendar(call.message, 'выезда')
                else:
                    bot.send_message(call.message.chat.id, 'Дата заезда должна быть больше или равна сегодняшней дате!'
                                                           'Повторите выбор даты!')
                    handlers.input_data.my_calendar(call.message, 'заезда')


def check_month_day(number: str) -> str:
    """
    Преобразование формата числа месяца или дня из формата 1..9 в формат 01..09
    : param number : str, число месяца или дня
    : return number : str
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if int(number) in numbers:
        number = '0' + number
    return number
