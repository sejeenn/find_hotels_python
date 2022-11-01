from loader import bot
from telebot.types import Message, CallbackQuery
from loguru import logger
from states.user_inputs import UserInputState
from utils.find_destination_id import find_city
from keyboards.inline import cities_buttons
from handlers.commands import second_step


@bot.message_handler(commands=['lowprice', 'hiprice', 'bestdeal'])
def start_search(message: Message) -> None:
    """
        В начале бот реагирует на три команды одинаков, затем изходя из
        запомненной команды, делается нужная пользователю сортировка.
        :param message: Сообщения пользователя
    """
    bot.set_state(message.from_user.id, UserInputState.command, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
        logger.info('Запоминаем выбранную команду')
        data['command'] = message.text
    bot.set_state(message.from_user.id, UserInputState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель: ")


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: Message) -> None:
    """
        Здесь пользователь вводит название интересующего его города, который бот запоминает и
        отправляет сообщение функцию find_city(message), проверить наличие города
        :param message:
    """
    logger.info('Запоминаем введенный город')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    logger.info(f'Получаем словарь с вариантами городов')
    possible_cities = find_city(message)
    # если длина словаря больше 0, то отправляем его в генератор кнопок с вариантами городов
    if len(possible_cities) > 0:
        cities_buttons.buttons_gen(message, possible_cities)
    else:
        bot.send_message(message.from_user.id, f'Не могу найти искомый город - {data["input_city"]}, введи еще раз!')

    @bot.callback_query_handler(func=lambda call: call.data.isdigit())
    def callback_query(call: CallbackQuery) -> None:
        """
        :param call: Inline клавиатура передает callback_data, в котором значится destination_id города
        который будет использоваться при дальнейшем API запросе, на поиск отелей в конкретном городе
        """
        if call.data:
            bot.set_state(message.from_user.id, UserInputState.destinationId, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_id:
                data_id['destination_id'] = call.data
            bot.delete_message(call.message.chat.id, call.message.message_id)
            # получили destination_id и можно переходить ко второму этапу поиска -
            # дальнейшему сбору данных от пользователя
            second_step.continue_input(message)
