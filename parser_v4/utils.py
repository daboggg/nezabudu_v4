import re
from datetime import datetime

from parser_v4.errors import DatetimeValueException, errors_translation


# удаляет все лишние пробелы в начале, середине и конце строки
def remove_extra_spaces(message: str) -> str:
    return " ".join(re.split("\s+", message.strip()))


# проверяет вхождение в диапазон для часов
def checking_hour_range(hour: int) -> int:
    if -1 < hour < 24:
        return hour
    raise DatetimeValueException("час должен быть в диапазоне 0..23")


# проверяет вхождение в диапазон для минут
def checking_minute_range(minute: int) -> int:
    if -1 < minute < 60:
        return minute
    raise DatetimeValueException("минута должна быть в диапазоне 0..59")


# проверяет вхождение в диапазон для дней в месяце
def checking_day_range(day: int, month: int) -> int:
    try:
        if datetime.now().replace(month=month, day=day):
            return day
    except ValueError as e:
        raise DatetimeValueException(errors_translation[str(e)])


# проверяет вхождение в диапазон для дней в месяце
def checking_day_of_month(day: int) -> int:
    if 0 < day < 32:
        return day
    raise DatetimeValueException("день находится вне диапазона для месяца")