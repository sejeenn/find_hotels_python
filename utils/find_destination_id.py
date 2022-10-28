import requests
import json
import re
from config_data import config
from telebot.types import Message
from typing import Tuple, Dict, Union
from loader import bot
from telebot import types

city_url = 'https://hotels4.p.rapidapi.com/locations/search'
headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def find_city(message: Message) -> Dict:
    querystring = {"query": message.text, "locale": "en_US", "currency": "USD"}
    response = requests.request("GET", city_url, headers=headers, params=querystring)
    data = json.loads(response.text)
    pattern = '<[^>]*>'
    # with open('step_1_rome.json', 'r') as file_rome:
    #     data = json.load(file_rome)
    with open('step_1.json', 'w') as file:
        json.dump(data, file, indent=4)

    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    return possible_cities


