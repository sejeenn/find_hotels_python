import database

input_data = {
    'command': '/lowprice', 'sort': 'PRICE_LOW_TO_HIGH', 'date_time': '13.03.2023 08:37:10',
    'chat_id': 732418186, 'input_city': 'baku', 'destination_id': '492', 'quantity_hotels': '3',
    'price_min': '35', 'price_max': '70', 'photo_need': 'yes', 'photo_count': '3',
    'checkInDate': {'day': '17', 'month': '03', 'year': '2023'},
    'checkOutDate': {'day': '24', 'month': '03', 'year': '2023'},
    'landmark_in': 0, 'landmark_out': 0
}
new_save = {732418186: {'destination_id': 492, 'date_time': '13.03.2023 14:35:01'}}
# database.write_to_bd.save_inputs(input_data)
# database.write_to_bd.save_search_history(search_result)

search_result = {
    'chat_id': 732418186, 'destination_id': 492, 'date_time': '13.03.2023 15:16:33',
    'hotels':
        {
        '21605456':
            {
            'name': 'Marine Inn Hotel Baku', 'address': 'Neftchiler Avenue 62, Baku, AZ1010',
            'price': 35.08, 'distance': 1.12, 'images': [
                'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/40ab9b4f.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/f0ec51e2.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/bde853af.jpg?impolicy=resizecrop&rw=500&ra=fit']
        },
        '83494845':
            {'name': 'AZNEFT SEASIDE  DELUXE APARTMENT', 'address': 'Adil Isgandarov 4, Baku, AZ1001',
             'price': 35.94, 'distance': 0.54, 'images': [
                'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/ba0063a6.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/ab860f7b.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/9c3c5693.jpg?impolicy=resizecrop&rw=500&ra=fit']
             },
        '22868360':
            {'name': 'City Apartments', 'address': 'Ismayil Hidayat Zadeh str.16, Baku, 1005',
             'price': 38.64, 'distance': 2.54, 'images': [
                'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/a636719a.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/14869b0b.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/c6f9c855.jpg?impolicy=resizecrop&rw=500&ra=fit']
             }
    }
}
print(search_result['chat_id']['hotels'])