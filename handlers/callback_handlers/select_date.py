from loader import bot
from loguru import logger
import datetime
from states.user_states import UserInputState
from keyboards.calendar.telebot_calendar import CallbackData, Calendar
from handlers.input_data import print_data
import handlers.input_data


calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call):
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
                print('Выбранная дата', select_date, 'CheckIn', checkin)
                if int(select_date) > checkin:
                    logger.info('Ввод и сохранение даты выезда.')
                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}
                    if data['sort'] == 'DISTANCE':
                        bot.set_state(call.message.chat.id, UserInputState.landmarkIn)
                        bot.send_message(call.message.chat.id, 'Введите начало диапазона расстояния от центра '
                                                               '(от 0 км).')
                    else:
                        print_data(call.message, data)
                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда должна быть больше даты заезда! '
                                                           'Повторите выбор даты!')
                    handlers.input_data.my_calendar(call.message, 'выезда')
            else:
                if int(select_date) >= int(now):
                    print('Выбранная дата заезда:', select_date, 'Сегодняшняя дата:', now)
                    logger.info('Ввод и сохранение даты заезда.')
                    data['checkInDate'] = {'day': day, 'month': month, 'year': year}
                    handlers.input_data.my_calendar(call.message, 'выезда')
                else:
                    bot.send_message(call.message.chat.id, 'Дата заезда должна быть больше или равна сегодняшней дате!'
                                                           'Повторите выбор даты!')
                    handlers.input_data.my_calendar(call.message, 'заезда')


def check_month_day(number):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if int(number) in numbers:
        number = '0' + number
    return number
