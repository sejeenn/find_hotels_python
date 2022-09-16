from loader import bot
from telebot import types
import utils.find_hotel
from states.user_inputs import UserInputState


def cities_buttons(message, possible_cities):
    # вывод возможных городов по запросу "rome" (Рим) step_1_rome.json
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data:
        selected_destination_id = call.data
        print('Выбран город destinationId:', selected_destination_id)  # сообщение в консоли
        bot.delete_message(call.message.chat.id, call.message.message_id)
        message = bot.send_message(call.from_user.id, 'Вы выбрали destinationId: ' + selected_destination_id)
        bot.register_next_step_handler(message, utils.find_hotel.get_dict_hotels(selected_destination_id))
