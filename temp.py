end_data = {
    'command': '/lowprice', 'sort': 'PRICE_LOW_TO_HIGH', 'date_time': '07.02.2023 11:06:27', 'chat_id': 732418186,
    'input_city': 'rome', 'destination_id': '553248633938945217', 'quantity_hotels': '3', 'price_min': '30',
    'price_max': '80', 'photo_need': 'yes', 'photo_count': '3', 'checkInDate': {
        'day': '17', 'month': '02', 'year': '2023'},
    'hotels':
        {

        '2057688':
        {
            'name': 'Hotel Filippo', 'address': 'Via Turati 163, Rome, RM, 185', 'price': '$69',
            'coordinates': {'latitude': '41.89566', 'longitude': '12.5073'},
            'images': [
                'https://images.trvl-media.com/lodging/3000000/2060000/2057700/2057688/60517596.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/3000000/2060000/2057700/2057688/60517596.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/3000000/2060000/2057700/2057688/969b67c3.jpg?impolicy=resizecrop&rw=500&ra=fit'
                ]
        }, '2525531':
        {
            'name': 'B&B Giovy Rome', 'address': 'Via Principe Amedeo 85 A, Rome, RM, 00185', 'price': '$86',
            'coordinates': {'latitude': '41.898248', 'longitude': '12.501277'},
            'images': [
                'https://images.trvl-media.com/lodging/3000000/2530000/2525600/2525531/282905d1.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/3000000/2530000/2525600/2525531/5511a3c3.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/3000000/2530000/2525600/2525531/9eae99c2.jpg?impolicy=resizecrop&rw=500&ra=fit']
        }, '12024222':
        {
            'name': 'İstanbul Fair Hotel',
            'address': 'Gültepe Mah.Gültepe Yanyol Sok.No:3, Küçükçekmece, Istanbul, Istanbul, 34295',
            'price': '$41', 'coordinates': {'latitude': '40.993499', 'longitude': '28.794301'},
            'images': [
                'https://images.trvl-media.com/lodging/13000000/12030000/12024300/12024222/3ef36c88.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/13000000/12030000/12024300/12024222/c2e73ac1.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/13000000/12030000/12024300/12024222/6fcc3670.jpg?impolicy=resizecrop&rw=500&ra=fit']
        }, '16131481':
        {
            'name': 'Express Inci Airport Hotel',
            'address': 'kartal tepe mahallesi, pamuk sokak no 13 sefaköy, Istanbul, küçükçekmece, 34100',
            'price': '$36', 'coordinates': {'latitude': '41.00052', 'longitude': '28.80059'},
            'images': [
                'https://images.trvl-media.com/lodging/17000000/16140000/16131500/16131481/513eade3.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/17000000/16140000/16131500/16131481/4981da10.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/17000000/16140000/16131500/16131481/8925015c.jpg?impolicy=resizecrop&rw=500&ra=fit']
        }, '25169838':
        {
            'name': 'Taksim Maxwell Hotel',
            'address': 'Hüseyinaga Mahallesi, Büyük Bayram sokak No 18 Taksim Beyoglu, Istanbul, Istanbul, 34435',
            'price': '$38', 'coordinates': {'latitude': '41.03541', 'longitude': '28.97884'},
            'images': [
                'https://images.trvl-media.com/lodging/26000000/25170000/25169900/25169838/9222d26f.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/26000000/25170000/25169900/25169838/27e43316.jpg?impolicy=resizecrop&rw=500&ra=fit',
                'https://images.trvl-media.com/lodging/26000000/25170000/25169900/25169838/095d914e.jpg?impolicy=resizecrop&rw=500&ra=fit']
                }
    }
}


sorted_end_data = sorted(end_data['hotels'].items(), key=lambda x: x[1]['price'])
# for i in end_data:
#     print(i)
print(sorted_end_data)