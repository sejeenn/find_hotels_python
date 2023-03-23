import sqlite3


connection = sqlite3.connect("test.sqlite3")
cursor = connection.cursor()


# пользователь запустил бота
user = {
    'chat_id': 732418186, 'username': 'sejeenn', 'full_name': 'Евгений Воронцов'
}

# пользователь сделал запрос
user_query = {
    'command': '/lowprice', 'sort': 'PRICE_LOW_TO_HIGH', 'date_time': '12.03.2023 19:40:11', 'chat_id': 732418186,
    'input_city': 'baku', 'destination_id': '492', 'quantity_hotels': '3', 'price_min': '35', 'price_max': '70',
    'photo_need': 'yes', 'photo_count': '3', 'checkInDate': {'day': '23', 'month': '03', 'year': '2023'},
    'checkOutDate': {'day': '30', 'month': '03', 'year': '2023'}, 'landmark_in': 0, 'landmark_out': 0
}

# пользователь получил ответ
user_response = {
    '21605456':
        {
            'name': 'Marine Inn Hotel Baku', 'address': 'Neftchiler Avenue 62, Baku, AZ1010',
            'price': 35.08, 'distance': 1.12, 'chat_id': 732418186, 'images': [
            'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/40ab9b4f.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/f0ec51e2.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/22000000/21610000/21605500/21605456/bde853af.jpg?impolicy=resizecrop&rw=500&ra=fit']
        },
    '83494845':
        {'name': 'AZNEFT SEASIDE  DELUXE APARTMENT', 'address': 'Adil Isgandarov 4, Baku, AZ1001',
         'price': 35.94, 'distance': 0.54, 'chat_id': 732418186, 'images': [
            'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/ba0063a6.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/ab860f7b.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/84000000/83500000/83494900/83494845/9c3c5693.jpg?impolicy=resizecrop&rw=500&ra=fit']
         },
    '22868360':
        {'name': 'City Apartments', 'address': 'Ismayil Hidayat Zadeh str.16, Baku, 1005',
         'price': 38.64, 'distance': 2.54, 'chat_id': 732418186, 'images': [
            'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/a636719a.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/14869b0b.jpg?impolicy=resizecrop&rw=500&ra=fit',
            'https://images.trvl-media.com/lodging/23000000/22870000/22868400/22868360/c6f9c855.jpg?impolicy=resizecrop&rw=500&ra=fit']
         }
}


def add_user(user_data):
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        chat_id INTEGER UNIQUE,
        username STRING,
        full_name TEXT
    );
    """)
    try:
        cursor.execute(
            "INSERT INTO user (chat_id, username, full_name) VALUES (?, ?, ?)",
            (user_data['chat_id'], user_data['username'], user_data['full_name'])
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Данный пользователь уже существует')


def add_query(query_data):
    cursor.execute("""CREATE TABLE IF NOT EXISTS query(
           id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
           user_id INTEGER,
           input_city STRING,
           photo_need STRING,
           destination_id STRING, 
           date_time STRING UNIQUE
       );
       """)

    try:
        cursor.execute(
            "INSERT INTO query(user_id, input_city, photo_need, destination_id, date_time) VALUES (?, ?, ?, ?, ?)",
            (user['chat_id'], query_data['input_city'], user_query['photo_need'], query_data['destination_id'],
             query_data['date_time'])
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Запрос с такой датой и временем уже существует')


def add_response(hotel_id, name, address, price, distance):
    cursor.execute("""CREATE TABLE IF NOT EXISTS response(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        query_id INTEGER,
        hotel_id STRING,
        name STRING,
        address STRING, 
        price REAL,
        distance REAL
    );
    """)
    cursor.execute(f"SELECT `id` FROM query WHERE `date_time` = ?", (user_query['date_time'],))
    query_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO response(query_id, hotel_id, name, address, price, distance) VALUES (?, ?, ?, ?, ?, ?)",
        (query_id, hotel_id, name, address, price, distance)
    )

    connection.commit()


def add_images(hotel_id, link_img):
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            hotel_id INTEGER REFERENCES response (id),
            link TEXT     
        );""")

    cursor.execute("INSERT INTO images (hotel_id, link) VALUES (?, ?)", (hotel_id, link_img))

    connection.commit()

#
# add_user(user)
# add_query(user_query)
# for hotel in user_response.items():
#     # add_response(hotel[0], hotel[1]['name'],
#     #              hotel[1]['address'], hotel[1]['price'], hotel[1]['distance'])
#     for link in hotel[1]['images']:
#         add_images(hotel[0], link)


cursor.execute(f"SELECT `date_time`, `input_city` FROM query WHERE `user_id` = ?", (user['chat_id'],))
records = cursor.fetchall()

for item in records:
    print(item)
# ('12.03.2023 19:40:11', 'baku') тут может быть не одна запись
# предлагается пользователю выбрать нужную ему дату чтобы программа получила нужный ключ по которому
# будут выбраны данные
key = int(input('Введи ключ: '))
cursor.execute("SELECT * FROM response WHERE `query_id` = ?", (key,))
hotels = cursor.fetchall()

cursor.execute("SELECT `photo_need` FROM query WHERE `id` = ?", (key,))
photo_need = cursor.fetchone()
answer = photo_need[0]


for hotel in hotels:
    print('Hotel ID:', hotel[2])
    print('Название отеля:', hotel[3])
    print('Адрес отеля:', hotel[4])
    print('Стоимость проживания:', hotel[5])
    print('Удаленность от центра:', hotel[6])
    if answer == 'yes':
        print('Если были нужны фотографии - выведем их!')
        cursor.execute("SELECT `link` FROM images WHERE `hotel_id` = ?", (hotel[2],))
        print(cursor.fetchall())
    else:
        print('Фотки были не нужны.')
    print()

connection.close()
