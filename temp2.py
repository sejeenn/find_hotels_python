import numpy as np


user_inputs = {'command': '/lowprice', 'sort': 'PRICE_LOW_TO_HIGH', 'date_time': '25.02.2023 09:47:31',
               'chat_id': 732418186, 'input_city': 'baku', 'destination_id': '492', 'quantity_hotels': '10',
               'price_min': '20', 'price_max': '100', 'photo_need': 'no', 'photo_count': '0',
               'checkInDate': {'day': '26', 'month': '02', 'year': '2023'},
               'checkOutDate': {'day': '28', 'month': '02', 'year': '2023'}
               }
hotels = {
    '87386584': {'name': 'North West Hotel', 'id': '87386584', 'distance': 6.08, 'unit': 'MILE', 'price': '$25'},
    '37732532': {'name': 'Mildom Hotel Baku', 'id': '37732532', 'distance': 1.32, 'unit': 'MILE', 'price': '$27'},
    '867426': {'name': 'Old City Inn Hotel', 'id': '867426', 'distance': 0.16, 'unit': 'MILE', 'price': '$27'},
    '45285213': {'name': 'Nizami Hotel', 'id': '45285213', 'distance': 0.17, 'unit': 'MILE', 'price': '$24'},
    '27764427': {'name': 'Flamingo Hotel Baku', 'id': '27764427', 'distance': 0.95, 'unit': 'MILE', 'price': '$25'},
    '76687347': {'name': 'Sahil Hotel Baku', 'id': '76687347', 'distance': 3.18, 'unit': 'MILE', 'price': '$25'},
    '44945431': {'name': 'AF Hotel City', 'id': '44945431', 'distance': 0.96, 'unit': 'MILE', 'price': '$26'},
    '36802189': {'name': 'Boutique Hotel Avenue', 'id': '36802189', 'distance': 0.47, 'unit': 'MILE', 'price': '$30'},
    '32930054': {'name': 'Royal Hotel', 'id': '32930054', 'distance': 3.05, 'unit': 'MILE', 'price': '$28'}
}
# {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
sorted_hotels = {
    key: value for key, value in sorted(hotels.items(), key=lambda hotel_id: hotel_id[1]['distance'])}
new_dict = {}
for keys in sorted_hotels:
    print(sorted_hotels[keys]['distance'])
    if sorted_hotels[keys]['distance'] in np.arange(0, 2, 0.01):
        new_dict[keys] = sorted_hotels[keys]
print(new_dict)
