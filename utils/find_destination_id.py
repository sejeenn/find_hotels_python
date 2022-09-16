import requests
import json
import re
from typing import Tuple, Dict, Union
from keyboards.inline.cities_buttons import cities_buttons
from loader import bot
from states.user_inputs import UserInputState


city_url = 'https://hotels4.p.rapidapi.com/locations/search'


def find_city(message):
    """Задаем поиск города и получаем словарь с возможными вариантами города
        (города иногда называются одинаково)"""
    # Временно не обращаемся к серверу, обойдемся локальными средствами
    # querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
    # response = requests.request("GET", city_url, headers=headers, params=querystring)
    # data = json.loads(response.text)

    # сохранение пользовательского ввода
    bot.set_state(message.from_user.id, UserInputState.input_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    print('Пользователь ввёл город:', data['input_city'], ', сохраним это.')

    """Открываем файл JSON с результатами запроса по Риму"""
    pattern = '<[^>]*>'
    with open('step_1_rome.json', 'r') as file_rome:
        data = json.load(file_rome)

    # создаем словарь possible_cities, в котором будут храниться destinationId(ключ) города и его описание(значение)
    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    # вывод словаря в тестовом режиме в терминал
    print(possible_cities)

    # отправляем полученный словарь в генератор инлайн кнопок
    cities_buttons(message, possible_cities)


