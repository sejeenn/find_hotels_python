from config_data import config
import requests
from telebot.types import InputMediaPhoto
import json

found_photos = []

with open('step_3_photos.json', 'r') as file:
    data = json.load(file)
    for index in range(3):
        print(data["hotelImages"][index]['baseUrl'].replace('{size}', 'y'))
        found_photos.append(data["hotelImages"][index]['baseUrl'].replace('{size}', 'y'))
    print(found_photos)
