import datetime
import calendar
import typing
from dataclasses import dataclass

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@dataclass
class Language:
    days: tuple
    months: tuple


RUSSIAN_LANGUAGE = Language(
    days=("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"),
    months=(
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ),
)


class Calendar:
    __lang: Language

    def __init__(self, language: Language = RUSSIAN_LANGUAGE):
        self.__lang = language

    def create_calendar(
        self,
        name: str = "calendar_1",
        year: int = None,
        month: int = None,
    ) -> InlineKeyboardMarkup:
        """
        Создание и постройка inline-клавиатуры с календарём.

        :param name:
        :param year: Year to use in the calendar if you are not using the current year.
        :param month: Month to use in the calendar if you are not using the current month.
        :return: Returns an InlineKeyboardMarkup object with a calendar.
        """
        now_day = datetime.datetime.now()
        if year is None:
            year = now_day.year
        if month is None:
            month = now_day.month

        calendar_callback = CallbackData(name, "action", "year", "month", "day")
        data_ignore = calendar_callback.new("IGNORE", year, month, "!")
        data_months = calendar_callback.new("MONTHS", year, month, "!")

        keyboard = InlineKeyboardMarkup(row_width=7)

        # Начальная шапка "месяц и год"
        keyboard.add(
            InlineKeyboardButton(
                self.__lang.months[month - 1] + " " + str(year),
                callback_data=data_months,
            )
        )

        # дни недели
        keyboard.add(
            *[
                InlineKeyboardButton(day, callback_data=data_ignore)
                for day in self.__lang.days
            ]
        )
        # переменная date_now для сравнения "сегодняшнего дня" с датой в календаре, дабы убрать из календаря
        # все даты которые меньше сегодняшней даты, дата в формате 20230331
        date_now = str(now_day.year) + check_month_day(str(now_day.month)) + check_month_day(str(now_day.day))
        # Вывод дней недели
        for week in calendar.monthcalendar(year, month):
            row = list()
            for day in week:
                date_calendar = str(year) + check_month_day(str(month)) + check_month_day(str(day))
                if day == 0 or int(date_calendar) < int(date_now):
                    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))

                # если сегодняшний день совпадает с днем в календаре, то этот день помещается в скобки
                elif (
                    f"{now_day.day}.{now_day.month}.{now_day.year}"
                    == f"{day}.{month}.{year}"

                ):
                    row.append(
                        InlineKeyboardButton(
                            f"(({day}))",
                            callback_data=calendar_callback.new(
                                "DAY", year, month, day
                            ),
                        )
                    )
                else:
                    row.append(
                        InlineKeyboardButton(
                            str(day),
                            callback_data=calendar_callback.new(
                                "DAY", year, month, day
                            ),
                        )
                    )
            keyboard.add(*row)

        # Вывод кнопок смены месяца
        keyboard.add(
            InlineKeyboardButton(
                "Предыдущий месяц",
                callback_data=calendar_callback.new("PREVIOUS-MONTH", year, month, "!"),
            ),
            InlineKeyboardButton(
                "Следующий месяц", callback_data=calendar_callback.new("NEXT-MONTH", year, month, "!")
            ),
        )

        return keyboard

    def create_months_calendar(
        self, name: str = "calendar", year: int = None
    ) -> InlineKeyboardMarkup:
        """
        Создает календарь с выбором месяца

        :param name:
        :param year:
        :return:
        """

        if year is None:
            year = datetime.datetime.now().year

        calendar_callback = CallbackData(name, "action", "year", "month", "day")

        keyboard = InlineKeyboardMarkup()

        for i, month in enumerate(
            zip(self.__lang.months[0::2], self.__lang.months[1::2])
        ):
            keyboard.add(
                InlineKeyboardButton(
                    month[0],
                    callback_data=calendar_callback.new("MONTH", year, 2 * i + 1, "!"),
                ),
                InlineKeyboardButton(
                    month[1],
                    callback_data=calendar_callback.new(
                        "MONTH", year, (i + 1) * 2, "!"
                    ),
                ),
            )

        return keyboard

    def calendar_query_handler(
        self,
        bot: TeleBot,
        call: CallbackQuery,
        name: str,
        action: str,
        year: int,
        month: int,
        day: int,
    ) -> None or datetime.datetime:
        """
        Метод создает новый календарь, если нажата кнопка "вперед" или "назад"
        Этот метод должен быть вызван внутри CallbackQueryHandler.


        :param bot: The object of the bot CallbackQueryHandler
        :param call: CallbackQueryHandler data
        :param day:
        :param month:
        :param year:
        :param action:
        :param name:
        :return: Returns a tuple
        """

        current = datetime.datetime(int(year), int(month), 1)
        if action == "IGNORE":
            bot.answer_callback_query(callback_query_id=call.id)
            return False, None
        elif action == "DAY":
            bot.delete_message(
                chat_id=call.message.chat.id, message_id=call.message.message_id
            )
            return datetime.datetime(int(year), int(month), int(day))
        elif action == "PREVIOUS-MONTH":
            preview_month = current - datetime.timedelta(days=1)
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name,
                    year=int(preview_month.year),
                    month=int(preview_month.month),
                ),
            )
            return None
        elif action == "NEXT-MONTH":
            next_month = current + datetime.timedelta(days=31)
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name, year=int(next_month.year), month=int(next_month.month)
                ),
            )
            return None
        elif action == "MONTHS":
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_months_calendar(name=name, year=current.year),
            )
            return None
        elif action == "MONTH":
            bot.edit_message_text(
                text=call.message.text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=self.create_calendar(
                    name=name, year=int(year), month=int(month)
                ),
            )
            return None
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="ERROR!")
            bot.delete_message(
                chat_id=call.message.chat.id, message_id=call.message.message_id
            )
            return None


class CallbackData:
    """
    Callback data factory
    """

    def __init__(self, prefix, *parts, sep=":"):
        if not isinstance(prefix, str):
            raise TypeError(
                f"Префикс должен быть экземпляром str, а не {type(prefix).__name__}"
            )
        if not prefix:
            raise ValueError("Префикс не должен быть пустым")
        if sep in prefix:
            raise ValueError(f"Разделитель {sep!r} не может использоваться в качестве префикса")
        if not parts:
            raise TypeError("Части не были переданы!")

        self.prefix = prefix
        self.sep = sep

        self._part_names = parts

    def new(self, *args, **kwargs) -> str:
        """
        Generate callback data

        :param args:
        :param kwargs:
        :return:
        """

        args = list(args)

        data = [self.prefix]

        for part in self._part_names:
            value = kwargs.pop(part, None)
            if value is None:
                if args:
                    value = args.pop(0)
                else:
                    raise ValueError(f"Значение для {part!r} не передано!")

            if value is not None and not isinstance(value, str):
                value = str(value)

            if not value:
                raise ValueError(f"Значение для части {part!r} не может быть пустым!'")
            if self.sep in value:
                raise ValueError(
                    f"Символ {self.sep!r} определяется как разделитель и не может использоваться в значениях частей"
                )

            data.append(value)

        if args or kwargs:
            raise TypeError("Было передано слишком много аргументов!")

        callback_data = self.sep.join(data)
        if len(callback_data) > 64:
            raise ValueError("Результат выполнения  callback_data слишком длинный!")

        return callback_data

    def parse(self, callback_data: str) -> typing.Dict[str, str]:
        """
        Анализ данных из callback data

        :param callback_data:
        :return:
        """

        prefix, *parts = callback_data.split(self.sep)

        if prefix != self.prefix:
            raise ValueError("Passed callback data can't be parsed with that prefix.")
        elif len(parts) != len(self._part_names):
            raise ValueError("Invalid parts count!")

        result = {"@": prefix}
        result.update(zip(self._part_names, parts))

        return result

    def filter(self, **config):
        """
        Создать фильтр

        :param config:
        :return:
        """

        for key in config.keys():
            if key not in self._part_names:
                return False

        return True


def check_month_day(number: str) -> str:
    """
    Преобразование формата числа месяца или дня из формата 1..9 в формат 01..09
    : param number : str, число месяца или дня
    : return number : str
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if int(number) in numbers:
        number = '0' + number
    return number
