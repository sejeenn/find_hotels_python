from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_states import UserInputState
from handlers.custom_handlers.input_data import my_calendar


@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def need_photo_callback(call: CallbackQuery) -> None:
    """
        Пользователь нажал кнопку "ДА" или "НЕТ"
        : param call: "yes" or "no"
        : return : None
        """
    if call.data == 'yes':
        logger.info(f'Нажата кнопка "ДА". User_id: {call.message.chat.id}')
        with bot.retrieve_data(call.message.chat.id) as data:
            data['photo_need'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserInputState.photo_count)
        bot.send_message(call.message.chat.id, 'Сколько вывести фотографий? От 1 до 10!')
    elif call.data == 'no':
        logger.info(f'Нажата кнопка "НЕТ". User_id: {call.message.chat.id} ')
        with bot.retrieve_data(call.message.chat.id) as data:
            data['photo_need'] = call.data
            data['photo_count'] = '0'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        my_calendar(call.message, 'заезда')

