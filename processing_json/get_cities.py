import json
from telebot.types import Dict


def get_city(response_text: str) -> Dict:
    """
    Принимает ответ от сервера с возможными вариантами городов. Возвращает словарь
    с названиями городов и их идентификатором.
    : param response_text : str текстовая строка, ответ от сервера
    : return possible_cities : Dict Возвращает словарь с вариантами городов
    """
    possible_cities = {}
    data = json.loads(response_text)
    if not data:
        raise LookupError('Запрос пуст...')
    for id_place in data['sr']:
        try:
            possible_cities[id_place['gaiaId']] = {
                "gaiaId": id_place['gaiaId'],
                "regionNames": id_place['regionNames']['fullName']
            }
        except KeyError:
            continue
    return possible_cities
