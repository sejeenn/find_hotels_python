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
           query_author INTEGER,
           date_time STRING UNIQUE,
           input_city STRING,
           destination_id STRING, 
           FOREIGN KEY (query_author) REFERENCES user (chat_id)
       );
       """)

    try:
        cursor.execute(
            "INSERT INTO query(query_author, date_time, input_city, destination_id) VALUES (?, ?, ?, ?)",
            (query_data['chat_id'], query_data['date_time'], query_data['input_city'], query_data['destination_id'])
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Запрос уже существует')


def add_response(chat_id, hotel_id, name, address, price, distance):
    cursor.execute("""CREATE TABLE IF NOT EXISTS response(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        chat_id INTEGER,
        hotel_id STRING,
        name STRING,
        address STRING, 
        price REAL,
        distance REAL,
        FOREIGN KEY (hotel_id) REFERENCES query (query_author)
    );
    """)
    cursor.execute(
        "INSERT INTO response(chat_id, hotel_id, name, address, price, distance) VALUES (?, ?, ?, ?, ?, ?)",
        (chat_id, hotel_id, name, address, price, distance)
    )

    connection.commit()


def add_images(link_img):
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            link TEXT,
            FOREIGN KEY (link) REFERENCES response (hotel_id)        
        );""")
    cursor.execute("INSERT INTO images (link) VALUES (?)", (link_img, ))

    connection.commit()


add_user(user)
add_query(user_query)
for hotel in user_response.items():
    add_response(hotel[1]['chat_id'], hotel[0], hotel[1]['name'],
                 hotel[1]['address'], hotel[1]['price'], hotel[1]['distance'])
    for link in hotel[1]['images']:
        print(link)

        add_images(link)


cursor.execute("SELECT * FROM response")
records = cursor.fetchall()
print()
# for hotel in records:
#     print("Название отеля:", hotel[3])
#     print("Адрес отеля:", hotel[4])
#     print("Стоимость проживания за ночь:", hotel[5])
#     print("Расстояние до центра:", hotel[6])
#     print()
connection.close()