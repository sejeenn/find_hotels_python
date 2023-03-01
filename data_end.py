data = {
    '18378713': {
        'hotel_id': '18378713', 'name': 'Yeni Hotel',
        'address': 'Nöbethane Cad.Dervisler Sok., No 12 Sirkeci Eminönü, Istanbul, Sirkeci, 34110',
        'price': '$33', 'coordinates': {'latitude': '41.014', 'longitude': '28.97794'}},
    '37197296': {
        'hotel_id': '37197296', 'name': 'The Zanadu İstanbul', 'address':
            'Sht. Mehmet Pasa Sk. 26/1, Kucuk Ayasofya Mahallesi Fatih, Istanbul, Sultanahmet, 34122',
        'price': '$60', 'coordinates': {'latitude': '41.004467', 'longitude': '28.971997'}},
    '9687040': {
        'hotel_id': '9687040', 'name': 'Istanbul Sydney Hotel', 'address':
            'Muhsine Hatun Mh Tavasi Cesme Sk No 45, Kumkapi, Istanbul, Istanbul, 34130',
        'price': '$34', 'coordinates': {'latitude': '41.004638', 'longitude': '28.96253'}},
    '83356913': {
        'hotel_id': '83356913', 'name': 'Kaifa Hotel',
        'address': 'Tavasi Çesme Sk. 74, Istanbul, Istanbul, 34130', 'price': '$34',
        'coordinates': {'latitude': '41.00373', 'longitude': '28.961848'}},
    '36366614': {'hotel_id': '36366614', 'name': 'The Lola Hotel',
                 'address': 'Katip Sinan Cami Sk., Istanbul, Istanbul, 34122',
                 'price': '$52', 'coordinates': {'latitude': '41.0057', 'longitude': '28.9715'}},
    '46385073': {'hotel_id': '46385073', 'name': 'Astra Boutique Hotel',
                 'address': 'Demirtas Mah., Hayriye Hanim Sk. No:22, Istanbul, Fatih, 34134', 'price': '$48',
                 'coordinates': {'latitude': '41.019092', 'longitude': '28.963749'}},
    '3525652': {'hotel_id': '3525652', 'name': 'Buhara Hotel',
                'address': 'Küçük Ayasofya Mah., Çardakl Frn Sok. No3 Sulatnahmet, Istanbul, Istanbul, 34122',
                'price': '$40', 'coordinates': {'latitude': '41.003846', 'longitude': '28.971668'}},
    '3089283': {'hotel_id': '3089283', 'name': 'Fors Hotel',
                'address': 'Piyerloti cad. Kadirga Hamam sk. No.10, Sultanahmet, Istanbul, Istanbul, 34490',
                'price': '$35', 'coordinates': {'latitude': '41.005506', 'longitude': '28.96851'}}
}

res2 = sorted(data.items(), key=lambda x: x[1]['price'])
print(res2)