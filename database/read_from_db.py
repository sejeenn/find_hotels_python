import sqlite3
from loguru import logger


def read_query() -> list:
    logger.info('Читаем таблицу query')
    connect = sqlite3.connect("database/history.sqlite3")
    cursor = connect.cursor()
    cursor.execute("SELECT `id`, `date_time`, `input_city` FROM query")
    records = cursor.fetchall()
    connect.close()
    return records


def get_history_response(query):
    logger.info('Читаем таблицу response.')
    connect = sqlite3.connect("database/history.sqlite3")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM response WHERE `query_id` = ?", query )
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

