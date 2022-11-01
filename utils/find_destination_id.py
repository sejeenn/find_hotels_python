import requests
import json
import re
from telebot.types import Message
from typing import Dict
from loader import bot
from config_data import config

city_url = 'https://hotels4.p.rapidapi.com/locations/search'
headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def find_city(message: Message) -> Dict:
    """

    :param message:
    :return: possible_cities
    Принимает от пользователя возможный вариант названия города, делает запрос к
    hotels.com и формирует словарь possible_cities с возможными вариантами городов.
    Так же используя регулярные выражения отсеиваем ненужную информацию из строки с описанием города
    """
    querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
    response = requests.request("GET", city_url, headers=headers, params=querystring)
    data = json.loads(response.text)
    pattern = '<[^>]*>'
    possible_cities = {}
    if 'message' in data:
        bot.send_message(message.from_user.id, f'Ошибка соединения с hotels.com\n{data["message"]}')
    else:
        try:
            for city in data['suggestions'][0]['entities']:
                possible_cities[city['destinationId']] = re.sub(pattern, '', city['caption'])
        except KeyError:
            print('Не найден ключ', KeyError)
    return possible_cities


