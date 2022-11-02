import requests
import json
from config_data import config
from telebot.types import Dict


def get_dict_hotels(querystring: Dict) -> Dict:
    """
        Принимает словарь, с формированным запросом к hotels.com и формирует ответ в виде
        словаря, с необходимыми параметрами отелей, для формирования отчета для пользователя.
        :param querystring
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    found_hotels = {}
    try:
        for hotel in data['data']['body']['searchResults']['results']:
            values = [hotel['name'], hotel['address']["streetAddress"], hotel['ratePlan']['price']['current'],
                      hotel['landmarks'], hotel["optimizedThumbUrls"]["srpDesktop"], hotel['id']]
            found_hotels[hotel['id']] = found_hotels.get(hotel['id'], values)
    except KeyError:
        print('Не найден ключ', KeyError)
    finally:
        return found_hotels
