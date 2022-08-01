import requests
import json
from config_data import config


def get_detail_info(hotel_id):
    """Получение детальной информации об отеле по его ID"""
    # url = "https://hotels4.p.rapidapi.com/properties/get-details"
    # querystring = {"id": hotel_id, "checkIn": "2022-08-15", "checkOut": "2022-08-20", "adults1": "1", "currency": "USD",
    #                "locale": "en_US"}
    # headers = {
    #     "X-RapidAPI-Key": config.RAPID_API_KEY,
    #     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    # }
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # data = json.loads(response.text)

    with open('step_3_rome.json', 'r') as file:
        data = json.load(file)
    # hotel_info = {}
    # for i_hotel in data['data']['body']['searchResults']['results']:
    #     found_hotels[i_hotel['id']] = i_hotel['name']
    return 'hotel_info'