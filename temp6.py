# import requests
#
# url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
#
# payload = "q=%D1%80%D0%B8%D0%BC"
# headers = {
# 	"content-type": "application/x-www-form-urlencoded",
# 	"Accept-Encoding": "application/gzip",
# 	"X-RapidAPI-Key": "25f90d3cdfmsh2cc6038b4e63c63p1d9fd5jsn2aad67a79b56",
# 	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
# }
#
# response = requests.request("POST", url, data=payload, headers=headers)
#
# print(response.text)

import googletrans
from googletrans import Translator

translator = Translator()
result = translator.translate('anytext')
