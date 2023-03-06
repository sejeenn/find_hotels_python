import json


def get_hotels(response_text, command, landmark_in, landmark_out):
    """
    Принимает ответ от сервера, выбранную команду сортировки, а так же пределы диапазона
    расстояния от центра города. Возвращает отсортированный словарь, в зависимости от команды сортировки.
    """
    data = json.loads(response_text)
    if not data:
        raise LookupError('Запрос пуст...')

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
