import logging
import re

from parser_v4.data import day_of_week, end_day_of_week, months, months_variants
from parser_v4.errors import DatetimeValueException
from parser_v4.reminder import Reminder
from parser_v4.utils import (remove_extra_spaces, checking_hour_range, checking_minute_range,
                             checking_day_range, checking_day_of_month)

logger = logging.getLogger(__name__)


def extract_date__time(message: str) -> Reminder:
    # словарь для значений времени {"year": 2, ...}
    tmp_dict = dict()
    period = ""

    # каждый "день" со временем или без
    if res := re.match(r".*(?P<date>(день|День)(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        tmp_dict["day"] = "*"
        tmp_dict["hour"] = 8
        tmp_dict["minute"] = 0
        period = f"каждый день в 8:00"
        if len(match_found_list) > 1:
            hour, minute = re.split(r":|-|\.", match_found_list[-1])
            tmp_dict["hour"] = checking_hour_range(int(hour))
            tmp_dict["minute"] = checking_minute_range(int(minute))
            period = f"каждый день в {hour}:{minute}"
        message = message.replace(res.group("date"), "")

    # каждый "понедельник-воскресенье" со временем или без
    elif res := re.match(f".*(?P<date>({'|'.join(day_of_week)})(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        tmp_dict["day_of_week"] = f"{day_of_week[match_found_list[0]]}"
        tmp_dict["hour"] = 8
        tmp_dict["minute"] = 0
        period = f"{end_day_of_week[match_found_list[0]]} в 8:00"
        if len(match_found_list) > 1:
            hour, minute = re.split(r":|-|\.", match_found_list[-1])
            tmp_dict["hour"] = checking_hour_range(int(hour))
            tmp_dict["minute"] = checking_minute_range(int(minute))
            period = f"{end_day_of_week[match_found_list[0]]} в {hour}:{minute}"
        message = message.replace(res.group("date"), "")

    # каждое "число, месяц" со временем или без
    elif res := re.match(f".*?(?P<date>(\d?\d\s+)({'|'.join(months_variants)})(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        tmp_dict["hour"] = 8
        tmp_dict["minute"] = 0
        if match_found_list[0].isdigit():
            tmp_dict["day"] = checking_day_range(int(match_found_list[0]), months_variants.get(match_found_list[1]))
            tmp_dict["month"] = months_variants.get(match_found_list[1])
            period = f"каждое {match_found_list[0]} {match_found_list[1]} в 8:00"
            if len(match_found_list) > 2:
                hour, minute = re.split(r":|-|\.", match_found_list[-1])
                tmp_dict["hour"] = checking_hour_range(int(hour))
                tmp_dict["minute"] = checking_minute_range(int(minute))
                period = f"каждое {match_found_list[0]} {match_found_list[1]} в {match_found_list[-1]}"
        message = message.replace(res.group("date"), "")

    # каждое "число месяца" со временем или без
    elif res := re.match(f".*?(?P<date>(\d?\d\s+)(число|числа|Число|Числа)(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        tmp_dict["hour"] = 8
        tmp_dict["minute"] = 0
        if match_found_list[0].isdigit():
            tmp_dict["day"] = checking_day_of_month(int(match_found_list[0]))
            period = f"каждое {match_found_list[0]} число в 8:00"
            if len(match_found_list) > 2:
                hour, minute = re.split(r":|-|\.", match_found_list[-1])
                tmp_dict["hour"] = checking_hour_range(int(hour))
                tmp_dict["minute"] = checking_minute_range(int(minute))
                period = f"каждое {match_found_list[0]} число в {match_found_list[-1]}"
        message = message.replace(res.group("date"), "")

    # если совпадений нет, выбросить исключение
    if not tmp_dict:
        raise DatetimeValueException("дата набрана неправильно, воспользуйтесь помощью")
    # удаляю лишние пробелы из строки
    message = remove_extra_spaces(message)
    logger.info(f"элементы datetime: {tmp_dict}")
    logger.info(f"message: {message}")
    logger.info(f"period: {period}")

    reminder = Reminder()
    reminder.params = {**tmp_dict, "trigger": "cron"}
    reminder.message = message
    reminder.period = period

    return reminder


def start(message: str) -> Reminder:
    return extract_date__time(message)
