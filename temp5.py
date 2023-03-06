import json

with open('distance_200result_size.json') as file:
    data = json.load(file)
hotels_data = {}
count = 0
for hotel in data['data']['propertySearch']["properties"]:

    if 1 < hotel['destinationInfo']['distanceFromDestination']['value'] < 7.5:
        hotels_data[hotel['id']] = {
            'name': hotel['name'], 'id': hotel['id'],
            'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
            'unit': hotel['destinationInfo']['distanceFromDestination']['unit'],
            'price': hotel['price']['lead']['amount']
        }
print(hotels_data)
print(count)
