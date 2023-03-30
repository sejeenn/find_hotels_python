from loader import bot
from telebot.types import CallbackQuery
from loguru import logger
from states.user_states import UserInputState


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку города, который ему нужен. Записываем id
    этого города и переходим к следующему шагу. Запрашиваем количество отелей для вывода в чат.
    : param call: получает id города
    : return : None
    """
    logger.info(f'Пользователь выбрал город. User_id: {call.message.chat.id}')
    if call.data:
        bot.set_state(call.message.chat.id, UserInputState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data['destination_id'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserInputState.quantity_hotels)
        bot.send_message(call.message.chat.id, 'Сколько вывести отелей в чат? Не более 25!')
