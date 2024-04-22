import logging
import re

from parser_v4.reminder import Reminder
from parser_v4.utils import (remove_extra_spaces, checking_hour_range, checking_minute_range)

logger = logging.getLogger(__name__)


def extract_date__time(message: str) -> Reminder:
    # словарь для значений времени {"year": 2, ...}
    tmp_dict = dict(day='last')
    period = ""

    if res := re.match(r".*?(?P<date>(\w\s)?\d?\d[-:.]\d\d).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")

        hour, minute = re.split(r":|-|\.", match_found_list[-1])
        tmp_dict["hour"] = checking_hour_range(int(hour))
        tmp_dict["minute"] = checking_minute_range(int(minute))
        period = f"каждый последний день месяца в {hour}:{minute}"

        message = message.replace(res.group("date"), "")
    else:
        tmp_dict["hour"] = 8
        tmp_dict["minute"] = 0
        period = f"каждый последний день месяца в 8:00"

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
    return extract_date__time(message.strip())
