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


def get_hotels(
        response_text: str,
        command: str,
        landmark_in: str,
        landmark_out: str
) -> Dict:
    """
    Принимает ответ от сервера, выбранную команду сортировки, а так же пределы диапазона
    расстояния от центра города. Возвращает отсортированный словарь, в зависимости от команды сортировки.
    : param response_text : str Ответ от сервера, в котором содержится информация об отелях
    : param command : str Команда сортировки
    : param landmark_in : str Начало диапазона растояния до центра
    : param landmark_out : str Конец диапазона растояния до центра
    : return hotels_data : Dict Возвращает словарь с данными об отелях
    """
    data = json.loads(response_text)
    if not data:
        raise LookupError('Запрос пуст...')
    # При поиске в некоторых городах выдается ошибка, я не очень понимаю из-за чего она.
    # Дабы ее исключить - эта проверка:
    if 'errors' in data.keys():
        return {'error': data['errors'][0]['message']}

    hotels_data = {}
    for hotel in data['data']['propertySearch']['properties']:
        try:
            hotels_data[hotel['id']] = {
                'name': hotel['name'], 'id': hotel['id'],
                'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
                'unit': hotel['destinationInfo']['distanceFromDestination']['unit'],
                'price': hotel['price']['lead']['amount']
            }
        except (KeyError, TypeError):
            continue
    # Сортируем по цене, от высокой стоимости, к меньшей.
    if command == '/highprice':
        hotels_data = {
            key: value for key, value in
            sorted(hotels_data.items(), key=lambda hotel_id: hotel_id[1]['price'], reverse=True)
        }
    # Обнуляем созданный ранее словарь и добавляем туда только те отели, которые соответствуют диапазону.
    elif command == '/bestdeal':
        hotels_data = {}
        for hotel in data['data']['propertySearch']["properties"]:
            if float(landmark_in) < hotel['destinationInfo']['distanceFromDestination']['value'] < float(landmark_out):
                hotels_data[hotel['id']] = {
                    'name': hotel['name'], 'id': hotel['id'],
                    'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
                    'unit': hotel['destinationInfo']['distanceFromDestination']['unit'],
                    'price': hotel['price']['lead']['amount']
                }

    return hotels_data


def hotel_info(hotels_request: str) -> Dict:
    """
    Принимает ответ от сервера с детальной информацией об отеле, и возвращает словарь с данными отеля.
    : param hotels_request : str Текстовый ответ от сервера о детальной информации об отеле.
    : return hotel_data: Dict Возвращает словарь с дополнительной информацией об отеле
    """
    data = json.loads(hotels_request)
    if not data:
        raise LookupError('Запрос пуст...')
    hotel_data = {
        'id': data['data']['propertyInfo']['summary']['id'], 'name': data['data']['propertyInfo']['summary']['name'],
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': data['data']['propertyInfo']['summary']['location']['coordinates'],
        'images': [
            url['image']['url'] for url in data['data']['propertyInfo']['propertyGallery']['images']

        ]
    }

    return hotel_data
