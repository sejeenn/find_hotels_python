from loader import bot
from telebot.types import Message
from utils.get_destination_id import search
from utils.find_hotel import get_dict_hotels
from utils.detail_info import get_detail_info


@bot.message_handler(commands=['lowprice'])
def survey(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти "
                                           "отель (в тестовом режиме это Рим(Rome).")

    # вывод возможных городов по запросу "rome" (Рим) step_1_rome.json
    destination_id = search(message.text)  # step_1_rome.json
    for key, value in destination_id.items():
        bot.send_message(message.from_user.id, value + ' : ID - ' + key)
    bot.send_message(message.from_user.id, 'Необходимо уточнить город назначения, '
                                           'введи ID наиболее подходящего города '
                                           '(в тестовом режиме это  ID - 10818945)')

    # Узнав точный ID города назначения мы можем поискать отели в этом городе, выведем его в чат
    hotels_id = get_dict_hotels('10818945')  # step_2_rome.json
    for key, value in hotels_id.items():
        bot.send_photo(message.from_user.id, value[4])
        bot.send_message(message.from_user.id, f'Название отеля: {value[0]}\nАдрес отеля: {value[1]}\n' +
                         f'Стоимость: {value[2]}\nРасстояние до: {value[3][0]["label"]} - {value[3][0]["distance"]}'
                         f'\nРасстояние до: {value[3][1]["label"]} - {value[3][1]["distance"]}\n'
                         f'ID - ' + str(key))

    # bot.send_message(message.from_user.id, 'Выберите нужный вам отель'
    #                                        '(в тестовом режиме это  ID - 613008448)')
    # Узнаем детальную информацию об конкретном отеле
    detail_info = get_detail_info('613008448')
    bot.send_message(message.from_user.id, detail_info)

