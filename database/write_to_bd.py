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
    try:
        cursor.execute(
            "INSERT INTO user (chat_id, username, full_name) VALUES (?, ?, ?)", (chat_id, username, full_name)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Данный пользователь уже существует')


def save_inputs(input_data):
    connection = sqlite3.connect("database/search_history.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_input(
        chat_id INT PRIMARY KEY,
        command TEXT,
        sort TEXT,
        date_time TEXT, 
        input_city TEXT,
        destination_id TEXT,
        quantity_hotels TEXT,
        price_min TEXT,
        price_max TEXT,
        photo_need TEXT,
        photo_count TEXT,
        day_in TEXT,
        month_in TEXT,
        year_in TEXT,
        day_out TEXT,
        month_out TEXT,
        year_out TEXT,
        landmark_in TEXT, 
        landmark_out TEXT);        
    """)
    cursor.execute("""INSERT INTO user_input VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (input_data['chat_id'], input_data['command'], input_data['sort'], input_data['date_time'],
         input_data['input_city'], input_data['destination_id'], input_data['quantity_hotels'],
         input_data['price_min'], input_data['price_max'], input_data['photo_need'],
         input_data['photo_count'], input_data['checkInDate']['day'],input_data['checkInDate']['month'],
         input_data['checkInDate']['year'], input_data['checkOutDate']['day'],
         input_data['checkOutDate']['month'], input_data['checkOutDate']['year'],
         input_data['landmark_in'], input_data['landmark_in']
         ))
    connection.commit()

    print(input_data)


def save_search_history(search_history):
    print(search_history)
    connection = sqlite3.connect("database/search_history.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS search_history(
            id INT PRIMARY KEY,
            name TEXT,
            address TEXT,
            price REAL,
            distance REAL);        
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(
                id INT PRIMARY KEY,
                links TEXT);        
            """)

    cursor.execute("""INSERT INTO search_history VALUES 
            (?, ?, ?, ?, ?)""",
                   (1, search_history['name'], search_history['address'],
                    search_history['price'], search_history['distance']
                    ))
    id = 1
    for link in search_history['images']:
        cursor.execute("INSERT INTO images VALUES (?, ?)", (id, link) )
        id += 1
    connection.commit()

