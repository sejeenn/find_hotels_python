from loader import bot
from telebot.types import Message
from telebot import types
import utils.find_destination_id
from keyboards.inline.cities_buttons import cities_buttons

from utils.find_hotel_lowprice import get_dict_hotels
from utils.detail_info import get_detail_info


@bot.message_handler(commands=['lowprice'])
def lowprice_handler(message: Message) -> None:
    """1. Город, где будет проводиться поиск."""
    # 1. Запрос города в котором ищем отель
    # 2. Городов может быть много, поэтому получаем словарь c destinationId и описанием
    # 3. Из представленных населенных пунктов выбираем нужный город (destinationId) нажимаем кнопку

    # запрос от пользователя города
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель: (Rome).")
    destination_id = bot.register_next_step_handler(message, utils.find_destination_id.find_city)
    print(destination_id)
