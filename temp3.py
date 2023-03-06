import requests
import json

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "6054439"},
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2022
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2022
    },
    "rooms": [
        {
            "adults": 2,
            "children": [{"age": 5}, {"age": 7}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "DISTANCE",
    "filters": {"price": {
        "max": 150,
        "min": 100
    }}
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "23208be4d8mshe2a3410fa44a25bp18d8afjsn04a562c7f27f",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


response = requests.request("POST", url, json=payload, headers=headers)
print(response.status_code)
data = response.json()
with open('distance_200result_size.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)


