import datetime
now = datetime.datetime.now()
print(type(now))
isinstance(now, datetime.datetime)
d = '24.03.2023 09:23:45'
print(len(d))

#  File "/home/eugene/PycharmProjects/python_basic_diploma/utils/print_data.py", line 40, in print_data
#     find_hotels.find_and_show_hotels(message, data)
#   File "/home/eugene/PycharmProjects/python_basic_diploma/utils/find_hotels.py", line 56, in find_and_show_hotels
#     hotels = processing_json.get_hotels.get_hotels(response_hotels.text, data['command'],
#   File "/home/eugene/PycharmProjects/python_basic_diploma/processing_json/get_hotels.py", line 20, in get_hotels
#     for hotel in data['data']['propertySearch']['properties']:
# TypeError: 'NoneType' object is not subscriptable