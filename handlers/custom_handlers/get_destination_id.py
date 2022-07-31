from loader import bot
from telebot import types
import requests
import json
import re
from typing import Tuple, Dict, Union

city_url = 'https://hotels4.p.rapidapi.com/locations/search'
def find_city(message):
    """Задаем поиск города и получаем словарь с возможными вариантами города
        (города иногда называются одинаково)"""

    # Временно не обращаемся к серверу, обойдемся локальными средствами
    # querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
    # response = requests.request("GET", city_url, headers=headers, params=querystring)
    # data = json.loads(response.text)

    """Открываем файл JSON с результатами запроса по Риму"""
    pattern = '<[^>]*>'
    with open('step_1_rome.json', 'r') as file_rome:
        data = json.load(file_rome)

    city_buttons = types.InlineKeyboardMarkup()
    for i in data['suggestions'][0]['entities']:
        city_buttons.add(
            types.InlineKeyboardButton(text=re.sub(pattern, '', i['caption']), callback_data=i['destinationId']))

    return city_buttons
