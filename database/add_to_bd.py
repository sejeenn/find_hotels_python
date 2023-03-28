import sqlite3
from loguru import logger


def add_user(chat_id: int, username: str, full_name: str) -> None:
    """
    Создает, если нужно, таблицу с данными пользователей:
    id, username и, если есть, "имя фамилия" и добавляет туда данные, если
    бота запускает новый пользователь. Данная таблица не участвует в выдаче сохраненной
    информации. Она просто хранит данные пользователя.
    : param chat_id : int
    : param username : str
    : param full_name : str
    : return : None
    """
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
        logger.info('Добавлен новый пользователь.')
        connection.commit()
    except sqlite3.IntegrityError:
        logger.info('Данный пользователь уже существует')
    connection.close()


def add_query(query_data: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    которые ввел пользователь для поиска
    : param query_data : dict
    : return : None
    """
    user_id = query_data['chat_id']
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS query(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER,
        date_time STRING, 
        input_city STRING,
        destination_id STRING,
        photo_need STRING,
        response_id INTEGER,
        FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE ON UPDATE CASCADE
    );    
    """)
    try:
        cursor.execute(
            "INSERT INTO query(user_id, input_city, photo_need, destination_id, date_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, query_data['input_city'], query_data['photo_need'], query_data['destination_id'],
             query_data['date_time'])
        )
        logger.info('Добавлен в БД новый запрос.')

        # Нам не нужно очень много записей историй поиска, поэтому для каждого пользователя
        # будем хранить только 5 последних записей, лишние - удалим.
        cursor.execute(f"""
                DELETE FROM query WHERE query.[date_time]=
                (SELECT MIN([date_time]) FROM query WHERE `user_id` = '{user_id}' )
                AND
                ((SELECT COUNT(*) FROM query WHERE `user_id` = '{user_id}' ) > 5 ) 
            """
                       )
        connection.commit()
    except sqlite3.IntegrityError:
        print('Запрос с такой датой и временем уже существует')


def add_response(search_result: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    которые бот получил в результате запросов к серверу.
    : param search_result : dict
    : return : None
    """
    connection = sqlite3.connect("database/history.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS response(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            query_id INTEGER,
            hotel_id STRING,
            name STRING,
            address STRING, 
            price REAL,
            distance REAL,
            FOREIGN KEY (hotel_id) REFERENCES images(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)
    for item in search_result.items():
        cursor.execute(f"SELECT `id` FROM query WHERE `date_time` = ?", (item[1]['date_time'],))
        query_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO response(query_id, hotel_id, name, address, price, distance) VALUES (?, ?, ?, ?, ?, ?)",
            (query_id, item[0], item[1]['name'], item[1]['address'], item[1]['price'], item[1]['distance'])
        )
        logger.info('Добавлены в БД данные отеля.')
        for link in item[1]['images']:
            cursor.execute("""CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            hotel_id INTEGER REFERENCES response (id),
            link TEXT     
            );""")
            cursor.execute("INSERT INTO images (hotel_id, link) VALUES (?, ?)", (item[0], link))
        logger.info('Добавлены в БД ссылки на фотографии отеля.')
        connection.commit()
    connection.close()
