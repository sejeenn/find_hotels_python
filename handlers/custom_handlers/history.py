from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import database
from states.user_states import UserInputState


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """
        Обработчик команд, срабатывает на команду /history
        Обращается к базе данных и выдает в чат запросы пользователя
        по отелям.
        : param message : Message
        : return : None
    """
    logger.info('Выбрана команда history!')
    queries = database.read_from_db.read_query(message.chat.id)
    logger.info(f'Получены записи из таблицы query:\n {queries}')
    for item in queries:
        bot.send_message(message.chat.id, f"({item[0]}). Дата и время: {item[1]}. Вы вводили город: {item[2]}")
    bot.set_state(message.chat.id, UserInputState.history_select)
    bot.send_message(message.from_user.id, "Введите номер интересующего вас варианта: ")


@bot.message_handler(state=UserInputState.history_select)
def input_city(message: Message) -> None:
    """
        Ввод пользователем номера запроса, которые есть в списке. Если пользователь введет
        неправильный номер или это будет "не цифры", то бот попросит повторить ввод.
        Запрос к базе данных нужных нам записей. Выдача в чат результата.
        : param message : Message
        : return : None
    """
    if message.text.isdigit():
        queries = database.read_from_db.read_query(message.chat.id)
        number_query = []
        photo_need = ''
        for item in queries:
            number_query.append(item[0])
            if int(message.text) == item[0] and item[3] == 'yes':
                photo_need = 'yes'

        if photo_need != 'yes':
            bot.send_message(message.chat.id, 'Пользователь выбирал вариант "без фото"')

        if int(message.text) in number_query:
            history_dict = database.read_from_db.get_history_response(message.text)
            logger.info('Выдаем результаты выборки из базы данных')
            for hotel in history_dict.items():
                medias = []
                caption = f"Название отеля: {hotel[1]['name']}]\n Адрес отеля: {hotel[1]['address']}" \
                          f"\nСтоимость проживания в " \
                          f"сутки $: {hotel[1]['price']}\nРасстояние до центра: {hotel[1]['distance']}"
                urls = hotel[1]['images']
                if photo_need == 'yes':
                    for number, url in enumerate(urls):
                        if number == 0:
                            medias.append(InputMediaPhoto(media=url, caption=caption))
                        else:
                            medias.append(InputMediaPhoto(media=url))
                    bot.send_media_group(message.chat.id, medias)
                else:
                    bot.send_message(message.chat.id, caption)
        else:
            bot.send_message(message.chat.id, 'Ошибка! Вы ввели число, которого нет в списке! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')
