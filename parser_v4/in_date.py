import re
import logging
from datetime import datetime, timedelta

from parser_v4.data import day_of_week, months, months_variants
from parser_v4.errors import DatetimeValueException, errors_translation
from parser_v4.reminder import Reminder
from parser_v4.utils import remove_extra_spaces

logger = logging.getLogger(__name__)


def extract_date__time(message: str) -> Reminder:
    now = datetime.now()
    hour = 8
    minute = 0
    result_datetime = None
    msg = None

    # в день недели со временем или без
    if res := re.match(f".*?(?P<date>(в\s+)?({'|'.join(day_of_week)})(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        msg = message.replace(match_found, "")

        if time := re.fullmatch("\d?\d[-:.]\d\d", match_found_list[-1].strip()):
            hour, minute, = re.split(r":|-|\.", time.group().strip())

        wd = day_of_week.get(match_found_list[0]) or day_of_week.get(match_found_list[1])

        tmp_datetime = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        if now.weekday() == int(wd):
            if tmp_datetime > now:
                result_datetime = tmp_datetime
            else:
                result_datetime = tmp_datetime + timedelta(days=7)
        else:
            while tmp_datetime.weekday() != int(wd):
                tmp_datetime = tmp_datetime + timedelta(days=1)
            result_datetime = tmp_datetime

    # число и месяц со временем или без
    elif res := re.match(f".*?(?P<date>(\d?\d\s+)({'|'.join(months_variants.keys())})(\s+\w*\s*\d?\d[-:.]\d\d)?).*",
                         message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        msg = message.replace(match_found, "")

        if time := re.fullmatch("\d?\d[-:.]\d\d", match_found_list[-1].strip()):
            hour, minute, = re.split(r":|-|\.", time.group().strip())
        day = int(match_found_list[0])
        month = months_variants.get(match_found_list[1])

        tmp_datetime = now.replace(day=day, month=month, hour=int(hour), minute=int(minute), second=0, microsecond=0)

        if now < tmp_datetime:
            result_datetime = tmp_datetime
        else:
            result_datetime = tmp_datetime.replace(year=now.year + 1)

    # полная дата со временем или без
    elif res := re.match(f".*?(?P<date>\d\d[-:.]\d\d[-:.]\d\d(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        msg = message.replace(match_found, "")

        if time := re.fullmatch("\d?\d[-:.]\d\d", match_found_list[-1].strip()):
            hour, minute, = re.split(r":|-|\.", time.group().strip())

        day, month, year = re.split(r":|-|\.", match_found_list[0])
        if len(year) == 2:
            year = '20' + year

        tmp_datetime = datetime(int(year), int(month), int(day), int(hour), int(minute))
        if now > tmp_datetime:
            raise DatetimeValueException("введенная дата раньше чем настоящая")
        result_datetime = tmp_datetime

    # завтра или послезавтра со временем или без
    elif res := re.match(f".*?(?P<date>(Послезавтра|послезавтра|Завтра|завтра)(\s+\w*\s*\d?\d[-:.]\d\d)?).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        msg = message.replace(match_found, "")

        if time := re.fullmatch("\d?\d[-:.]\d\d", match_found_list[-1].strip()):
            hour, minute, = re.split(r":|-|\.", time.group().strip())

        tmp_datetime = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

        if match_found_list[0].lower() == 'завтра':
            result_datetime = tmp_datetime + timedelta(days=1)
        else:
            result_datetime = tmp_datetime + timedelta(days=2)

    # завтра или послезавтра со временем или без
    elif res := re.match(f".*?(?P<date>(\w\s)?\d?\d[-:.]\d\d).*", message):
        match_found = remove_extra_spaces(res.group("date"))
        match_found_list = match_found.split(" ")
        msg = message.replace(match_found, "")

        if len(match_found_list) == 1:
            hour, minute, = re.split(r":|-|\.", match_found_list[0])
        else:
            hour, minute, = re.split(r":|-|\.", match_found_list[-1])

        tmp_datetime = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

        if now > tmp_datetime:
            result_datetime = tmp_datetime + timedelta(days=1)
        else:
            result_datetime = tmp_datetime

    # если совпадений нет, выбросить исключение
    if not result_datetime:
        raise DatetimeValueException("дата набрана неправильно, воспользуйтесь помощью")

    # удаляю лишние пробелы из строки
    msg = remove_extra_spaces(msg)

    logger.info(f"datetime: {result_datetime}")
    logger.info(f"message: {msg}")

    reminder = Reminder()
    reminder.params = {"run_date": result_datetime, "trigger": "date"}
    reminder.message = msg

    return reminder


def start(message: str) -> Reminder:
    try:
        return extract_date__time(remove_extra_spaces(message))
    except ValueError as e:
        raise DatetimeValueException(errors_translation.get(str(e)))
