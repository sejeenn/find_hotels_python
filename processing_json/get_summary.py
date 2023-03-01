import json


def hotel_info(hotels_request):
    data = json.loads(hotels_request)
    if not data:
        raise LookupError('Запрос пуст...')
    hotel_data = {
        'id': data['data']['propertyInfo']['summary']['id'], 'name': data['data']['propertyInfo']['summary']['name'],
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': data['data']['propertyInfo']['summary']['location']['coordinates']
                  }
    hotel_images = []
    for url in data['data']['propertyInfo']['propertyGallery']['images']:
        hotel_images.append(url['image']['url'])

    return hotel_data, hotel_images