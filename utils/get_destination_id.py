from loader import bot
from telebot import types
import requests
import json
import re
from typing import Tuple, Dict, Union

city_url = 'https://hotels4.p.rapidapi.com/locations/search'


def search(message):
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

    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    return possible_cities
