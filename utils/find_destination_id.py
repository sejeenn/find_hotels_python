import requests
import json
import re
from typing import Tuple, Dict, Union
from keyboards.inline.cities_buttons import cities_buttons
from loader import bot
from states.user_inputs import UserInfoState

city_url = 'https://hotels4.p.rapidapi.com/locations/search'


def find_city(message):
    """Задаем поиск города и получаем словарь с возможными вариантами города
        (города иногда называются одинаково)"""
    # сохраняем то что ввел пользователь в качестве города
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    print(data['input_city'])

    # Временно не обращаемся к серверу, обойдемся локальными средствами
    # querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
    # response = requests.request("GET", city_url, headers=headers, params=querystring)
    # data = json.loads(response.text)
    """Открываем файл JSON с результатами запроса по Риму"""
    pattern = '<[^>]*>'
    with open('step_1_rome.json', 'r') as file_rome:
        data = json.load(file_rome)

    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])

    cities_buttons(message, possible_cities)


