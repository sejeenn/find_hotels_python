from loader import bot
from telebot.types import Message
from loguru import logger
import datetime
from states.user_inputs import UserInputState
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from keyboards.calendar import main_calendar
from handlers.commands import third_step

calendar = Calendar(language=RUSSIAN_LANGUAGE)
from telebot.types import ReplyKeyboardRemove, CallbackQuery

calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


def continue_input(message: Message):
    """
        :param message:
        Начало второго этапа поиска, ввод данных от пользователя
    """
    logger.info('Перешли ко второму этапу ввода данных')
    bot.set_state(message.from_user.id, UserInputState.pageSize, message.chat.id)
    bot.send_message(message.from_user.id, 'Сколько отелей на странице вывести? Максимум 25')


@bot.message_handler(state=UserInputState.pageSize)
def input_page_size(message: Message) -> None:
    """

    :param message:
        Пользователь вводит количество отелей от 1 до 25, если ввод не цифра и не входит в
        заданные рамки, предлагается выбрать еще раз. При правильном вводе, последует переход
        к следующей функции обработки ввода.
    """
    try:
        if 0 < int(message.text) < 25:
            logger.info('сохранение количества отелей')
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['page_size'] = message.text
            bot.set_state(message.from_user.id, UserInputState.priceMin, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите минимальную стоимость номера, в долларах США')
        else:
            bot.send_message(message.from_user.id, 'Число должно быть в границах от 1 до 25!')
    except ValueError:
        bot.send_message(message.from_user.id, 'Ввод должен состоять из цифр')


@bot.message_handler(state=UserInputState.priceMin)
def input_price_min(message: Message) -> None:
    """
        Ввод минимальной стоимости номера за сутки, осуществляется исключительно в цифрах!
        :param message
    """
    logger.info('Ввод минимальной стоимости номера')
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = message.text
        bot.set_state(message.from_user.id, UserInputState.priceMax, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите максимальную стоимость номера в долларах США')
    else:
        bot.send_message(message.from_user.id, 'Ввод должен состоять из цифр')


@bot.message_handler(state=UserInputState.priceMax)
def input_price_max(message: Message) -> None:
    """
            Ввод максимальной стоимости номера за сутки, осуществляется исключительно в цифрах!
            :param message
        """
    logger.info('Ввод максимальной стоимости номера')
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_max'] = message.text
        bot.set_state(message.from_user.id, UserInputState.photo_need, message.chat.id)
        bot.send_message(message.from_user.id, 'Нужно ли вывести фотографии (Yes/No или Да/Нет)?')
    else:
        bot.send_message(message.from_user.id, 'Ввод должен состоять из цифр')


@bot.message_handler(state=UserInputState.photo_need)
def need_photo(message: Message) -> None:
    """
        :param message:
       Узнаем от пользователя о надобности или ненадобности фотографий в результате поиска
    """
    logger.info('Спрашиваем пользователя о надобности фотографий')
    answer_yes = ('Yes', 'yes', 'YES', 'ДА', 'Да', 'да')
    answer_no = ('No', 'no', 'NO', 'НЕТ', 'Нет', 'нет')
    # если ответ пользователя положительный (yes / да), то сохраняем его ответ и
    # спрашиваем его о количестве фотографий
    if message.text in answer_yes:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_need'] = message.text
        bot.set_state(message.from_user.id, UserInputState.photo_count, message.chat.id)
        bot.send_message(message.from_user.id, 'Сколько фотографий вывести (от 1 до 10) ?')
    # иначе просто сохраняем ответ, а счетчику фотографий присваиваем значение '0'
    elif message.text in answer_no:
        main_calendar.calendar_date(message, 'Выберите дату заезда:')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_need'] = message.text
            data['photo_count'] = '0'

    @bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
    def check_in(call: CallbackQuery):
        """Обработчик callback вызываемых клавиатур для выбора даты заезда или выезда
        используется готовый модуль telebot-calendar
        :param call: CallbackQuery
        """
        name, action, year, month, day = call.data.split(calendar_1_callback.sep)
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
        if action == "DAY":
            bot.send_message(chat_id=call.from_user.id, text=f"{date.strftime('%Y-%m-%d')}",
                             reply_markup=ReplyKeyboardRemove())

            # проверка того куда записать полученную дату с inline-клавиатуры
            now_date = int(datetime.datetime.now().strftime('%Y%m%d'))
            select_date = int(date.strftime('%Y%m%d'))
            bot.set_state(message.from_user.id, UserInputState.checkIn, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_end:
                # если ключа check_in еще не существует, то создаем его, а так же проверяем
                # чтобы дата заезда была не раньше "сегодня", а дата выезда не была меньше
                # даты заезда
                if 'check_in' in data_end:
                    checkin = int(''.join(data_end['check_in'].split('-')))
                    if select_date > checkin:
                        bot.send_message(message.from_user.id, 'Записал дату выезда:')
                        data_end['check_out'] = date.strftime('%Y-%m-%d')
                        # Записали дату выезда, переходим к заключительному этапу
                        third_step.finish_him(message, data_end)
                    else:
                        bot.send_message(message.from_user.id, 'Дата выезда должна быть больше '
                                                               'даты заезда, введи еще раз!')
                        main_calendar.calendar_date(message, 'Выберите дату выезда')
                else:
                    if select_date >= now_date:
                        data_end['check_in'] = date.strftime('%Y-%m-%d')
                        bot.send_message(message.from_user.id, 'Записал дату заезда:')
                        main_calendar.calendar_date(message, 'Выберите дату выезда')
                    else:
                        bot.send_message(message.from_user.id, 'Дата заезда должна быть больше '
                                                               'или равна сегодняшней дате, введи еще раз!')
                        main_calendar.calendar_date(message, 'Выберите дату заезда')

        elif action == "CANCEL":
            bot.send_message(chat_id=call.from_user.id, text="Cancellation",
                             reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.from_user.id, 'Вы собираетесь ручками дату вводить?!, Так не пойдет!')
            main_calendar.calendar_date(message, 'Выберите дату снова:')


@bot.message_handler(state=UserInputState.photo_count)
def photo_count(message: Message) -> None:
    """
        Ввод от пользователя о количестве фотографий и проверка их количества от 1 до 10
        и переход к выбору даты заезда.

        :param message
    """
    logger.info('Пользователю нужны фотографии, записываем их количество')
    try:
        if 0 < int(message.text) < 11:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as photo:
                photo['photo_count'] = message.text
            main_calendar.calendar_date(message, 'Выберите дату заезда:')
        else:
            bot.send_message(message.from_user.id, 'Число должно быть в границах от 1 до 10!')
    except ValueError:
        bot.send_message(message.from_user.id, 'Ввод должен состоять из цифр!')



