import requests
import json
import re
from config_data import config


def get_dict_hotels(destinationid):
    """Получаем слоарь отелей выбранного нами города"""
    # временно убираем связь с сервером, ограничившись скачанным JSON ответом сервера
    # url = "https://hotels4.p.rapidapi.com/properties/list"
    # querystring = {"destinationId": destinationid, "pageNumber": "1", "pageSize": "5", "checkIn": "2020-08-15",
    #                "checkOut": "2022-08-20", "adults1": "1", "priceMin": "10", "priceMax": "50",
    #                "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}
    # headers = {
    #     "X-RapidAPI-Key": config.RAPID_API_KEY,
    #     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    # }
    # print(destinationid)
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # data = json.loads(response.text)
    # with open('step_2_rome.json', 'w') as file:
    #     json.dump(data, file, indent=4)

    with open('step_2_rome.json', 'r') as file:
        data = json.load(file)

    found_hotels = {}
    for i_hotel in data['data']['body']['searchResults']['results']:
        values = [i_hotel['name'], i_hotel['address']["streetAddress"], i_hotel['ratePlan']['price']['current'],
                  i_hotel['landmarks']]
        found_hotels[i_hotel['id']] = found_hotels.get(i_hotel['id'], values)
    print(found_hotels)
    return found_hotels
