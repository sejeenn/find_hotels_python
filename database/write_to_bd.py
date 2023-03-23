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
    # {'2538925': {'name': 'Al Manzel Hotel Apartments', 'address': 'Zayed The 1st Street, PO Box 129666, Abu Dhabi',
    # 'price': 105.919254, 'distanse': 0.78, 'images': [
    # 'https://images.trvl-media.com/lodging/3000000/2540000/2539000/2538925/1187c729.jpg?impolicy=resizecrop&rw=500
    # &ra=fit', 'https://images.trvl-media.com/lodging/3000000/2540000/2539000/2538925/c4b30670.jpg?impolicy
    # =resizecrop&rw=500&ra=fit', 'https://images.trvl-media.com/lodging/3000000/2540000/2539000/2538925/ec95a28f.jpg
    # ?impolicy=resizecrop&rw=500&ra=fit']}}
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS response(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            query_id INTEGER,
            hotel_id INTEGER,
            name STRING,
            address STRING, 
            price REAL,
            distance REAL
        );
        """)
    connection.close()