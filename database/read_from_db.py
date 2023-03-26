import sqlite3
from loguru import logger


def read_query(user: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    logger.info('Читаем таблицу query')
    connect = sqlite3.connect("database/history.sqlite3")
    cursor = connect.cursor()
    cursor.execute("SELECT `id`, `date_time`, `input_city`, `photo_need` FROM query WHERE `user_id` = ?", (user,))
    records = cursor.fetchall()
    connect.close()
    return records


def get_history_response(query: str) -> dict:
    """
       Принимает id-запроса, обращается к базе данных и выдает данные которые нашел бот для
       пользователя по его запросам.
       : param query : str
       : return : dict
    """
    logger.info('Читаем таблицу response.')
    connect = sqlite3.connect("database/history.sqlite3")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM response WHERE `query_id` = ?", (query,))
    records = cursor.fetchall()
    history = {}
    for item in records:
        hotel_id = item[2]
        history[item[2]] = {'name': item[3], 'address': item[4], 'price': item[5], 'distance': item[6]}
        cursor.execute("SELECT * FROM images WHERE `hotel_id` = ?", (hotel_id, ))
        images = cursor.fetchall()
        links = []
        for link in images:
            links.append(link[2])
        history[item[2]]['images'] = links
    connect.close()
    return history

