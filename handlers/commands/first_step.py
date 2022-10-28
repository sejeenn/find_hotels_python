from loader import bot
from telebot.types import Message
from loguru import logger
from states.user_inputs import UserInputState
from utils.find_destination_id import find_city
from keyboards.inline import cities_buttons
from handlers.commands import second_step


@bot.message_handler(commands=['lowprice', 'hiprice', 'bestdeal'])
def start_search(message: Message) -> None:
    # Начало поиска отелей по разным командам. Сохраним выбранную команду пользователем.
    # Перед тем как производить поиск, узнаем, существует ли запрошенный город пользователем.
    logger.info('Запоминаем выбранную команду')
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
    bot.set_state(message.from_user.id, UserInputState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель: ")


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: Message) -> None:
    # Пользователь вводит название города
    logger.info('Запоминаем введенный город')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    # получаем словарь возможных городов
    possible_cities = find_city(message)
    logger.info(f'Получаем словарь с вариантами городов')
    # если длина словаря больше 1, то отправляем его в генератор кнопок
    if len(possible_cities) > 1:
        cities_buttons.buttons_gen(message, possible_cities)
    elif len(possible_cities) == 1:
        bot.send_message(message.from_user.id, 'Город всего один')
        # в будущем нужно написать обработчик для одного города
    else:
        bot.send_message(message.from_user.id, 'Не могу найти искомый город...' + data['command'])


    @bot.callback_query_handler(func=lambda call: call.data.isdigit())
    def callback_query(call):
        if call.data:
            bot.set_state(message.from_user.id, UserInputState.destinationId, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_id:
                data_id['destination_id'] = call.data
            bot.delete_message(call.message.chat.id, call.message.message_id)
            second_step.continue_input(message)
