import sqlite3


def add_user(chat_id, username, full_name):
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        chat_id INTEGER UNIQUE,
        username STRING,
        full_name TEXT
    );
    """)
    connection.commit()
    try:
        cursor.execute(
            "INSERT INTO user (chat_id, username, full_name) VALUES (?, ?, ?)", (chat_id, username, full_name)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Данный пользователь уже существует')
    connection.close()


def add_query(query_data):
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS query(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER,
        date_time STRING, 
        input_city STRING,
        destination_id STRING,
        photo_need STRING
    );    
    """)
    try:
        cursor.execute(
            "INSERT INTO query(user_id, input_city, photo_need, destination_id, date_time) VALUES (?, ?, ?, ?, ?)",
            (query_data['chat_id'], query_data['input_city'], query_data['photo_need'], query_data['destination_id'],
             query_data['date_time'])
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Запрос с такой датой и временем уже существует')


def add_response(search_result):
    print(search_result)
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
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
    for item in search_result.items():
        cursor.execute(f"SELECT `id` FROM query WHERE `date_time` = ?", (item[1]['date_time'],))
        query_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO response(query_id, hotel_id, name, address, price, distance) VALUES (?, ?, ?, ?, ?, ?)",
            (query_id, item[0], item[1]['name'], item[1]['address'], item[1]['price'], item[1]['distance'])
        )
        for link in item[1]['images']:
            add_images(item[0], link)
        connection.commit()
    connection.close()


def add_images(hotel_id, link_img):
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            hotel_id INTEGER REFERENCES response (id),
            link TEXT     
        );""")

    cursor.execute("INSERT INTO images (hotel_id, link) VALUES (?, ?)", (hotel_id, link_img))
    connection.commit()
