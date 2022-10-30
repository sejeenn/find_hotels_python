import requests
from config_data import config
import requests
import json

url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def get_photo(hotel_id, photo_count):
    querystring = {"id": hotel_id, "reviewOrder": "date_newest_first", "tripTypeFilter": "all"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    with open('step_3_photos.json', 'w') as file:
        json.dump(data, file, indent=4)
    found_photos = []

    for index in range(photo_count):
        found_photos.append(data["hotelImages"][index]['baseUrl'].replace('{size}', 'y'))

    return found_photos

