import requests
import json
import re
from config_data import config


def get_dict_hotels(querystring):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    with open('step_2.json', 'w') as file:
        json.dump(data, file, indent=4)
    found_hotels = {}
    for i_hotel in data['data']['body']['searchResults']['results']:
        values = [i_hotel['name'], i_hotel['address']["streetAddress"], i_hotel['ratePlan']['price']['current'],
                  i_hotel['landmarks'], i_hotel["optimizedThumbUrls"]["srpDesktop"]]
        found_hotels[i_hotel['id']] = found_hotels.get(i_hotel['id'], values)
    return found_hotels
