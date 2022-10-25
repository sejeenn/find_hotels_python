from loader import bot
from telebot import types
from datetime import date
from keyboards.calendar.keyboards import generate_calendar_days, generate_calendar_months, EMTPY_FIELD
from keyboards.calendar.filters import calendar_factory, calendar_zoom, bind_filters


@bot.message_handler(commands='calendar')
def calendar_command_handler(message: types.Message):
    now = date.today()
    bot.send_message(message.from_user.id, 'Выбери дату:',
                     reply_markup=generate_calendar_days(year=now.year, month=now.month))

#
# @bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter())
# def calendar_action_handler(call: types.CallbackQuery):
#     callback_data: dict = calendar_factory.parse(callback_data=call.data)
#     year, month = int(callback_data['year']), int(callback_data['month'])
#
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
#                                   reply_markup=generate_calendar_days(year=year, month=month))
#     print('1', call.data)
#
#
# @bot.callback_query_handler(func=None, calendar_zoom_config=calendar_zoom.filter())
# def calendar_zoom_out_handler(call: types.CallbackQuery):
#     callback_data: dict = calendar_zoom.parse(callback_data=call.data)
#     year = int(callback_data.get('year'))
#
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
#                                   reply_markup=generate_calendar_months(year=year))
#     print('2', call.data)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_empty_field_handler(call: types.CallbackQuery):
#     # bot.send_message(call.message.from_user.id, call.data)
#     print(call.data)
