import requests
import json
import re
from typing import Tuple, Dict, Union
from loader import bot
from telebot import types
from states.user_inputs import UserInputState

city_url = 'https://hotels4.p.rapidapi.com/locations/search'


def find_city(message):
    """
        1. Функция принимает пользовательский ввод (город)
        2. Делает запрос исходя из запроса пользователя либо к серверу hotels.com, либо локально
            создаем словарь с возможными городами
        3. Отправляем в чат кнопки с возможными вариантами города
        4. Возвращаем конкретный destination_id туда откуда была вызвана функция
    """

    # Открываем файл JSON с результатами запроса по Риму (временно)
    pattern = '<[^>]*>'
    with open('step_1_rome.json', 'r') as file_rome:
        data = json.load(file_rome)

    # создаем словарь possible_cities, в котором будут храниться destinationId(ключ) города и его описание(значение)
    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    # вывод словаря в тестовом режиме в терминал
    print(possible_cities)

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
            bot.send_message(call.from_user.id, 'Вы выбрали destinationId: ' + selected_destination_id)
            return selected_destination_id

# Временно не обращаемся к серверу, обойдемся локальными средствами
# querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
# response = requests.request("GET", city_url, headers=headers, params=querystring)
# data = json.loads(response.text)

# сохранение пользовательского ввода
# bot.set_state(message.from_user.id, UserInputState.input_city, message.chat.id)
# with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#     data['input_city'] = message.text
# print('Пользователь ввёл город:', data['input_city'], ', сохраним это.')
