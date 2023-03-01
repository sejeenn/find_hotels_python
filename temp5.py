import json

with open("distance.json", "r") as read_file:
    data = json.load(read_file)

for hotel in data['data']['propertySearch']['properties']:
    print(hotel['price']['lead']['amount'])


