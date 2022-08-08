from loader import bot
from telebot import types
from states.user_inputs import UserInfoState


def cities_buttons(message, possible_cities):
    # вывод возможных городов по запросу "rome" (Рим) step_1_rome.json
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data:
        temp = call.data

        # bot.set_state(call.from_user.id, UserInfoState.press_button_city, call.chat.id)
        # with bot.retrieve_data(call.from_user.id, call.chat.id) as data1:
        #     data1['press_button_city'] = call.data
        # print(data1['press_button_city'])
