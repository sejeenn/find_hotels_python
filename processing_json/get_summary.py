import json
from telebot.types import Dict


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
