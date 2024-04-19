import logging
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta

from parser_v4.data import through_data
from parser_v4.errors import DatetimeValueException
from parser_v4.reminder import Reminder
from parser_v4.utils import remove_extra_spaces

logger = logging.getLogger(__name__)


# выделяет временные метки из сообщения
def extract_date__time(message: str) -> tuple[str, dict[str, int]]:
    # словарь для значений времени {"year": 2, ...}
    tmp_dict = dict()

    parts_of_time = through_data.keys()

    for part_of_time in parts_of_time:
        variants = through_data.get(part_of_time) + [item.capitalize() for item in through_data.get(part_of_time)]
        pattern = f".*?(?P<num>(\d+)?(^|\W)({'|'.join(variants)})).*"
        try:
            result = re.fullmatch(pattern, message)
            match_found = result.group("num").strip()
            match_found_list = match_found.split(" ")
            if len(match_found_list) == 2:
                tmp_dict[part_of_time] = int(match_found_list[0])
            else:
                tmp_dict[part_of_time] = 1
            message = message.replace(match_found, "")
        except Exception as e:
            pass
    if not tmp_dict:
        raise DatetimeValueException("дата набрана неправильно, воспользуйтесь помощью")
    # удаляю лишние пробелы из строки
    message = remove_extra_spaces(message)
    logger.info(f"элементы datetime: {tmp_dict}")
    logger.info(f"message: {message}")
    return message, tmp_dict


def create_datetime(date__time_dict: dict[str, int]) -> datetime:
    dt = datetime.now() + relativedelta(**date__time_dict)
    logger.info(f"созданная дата-время: {dt}")
    return dt


def start(message: str) -> Reminder:
    msg, date__time_dict, = extract_date__time(remove_extra_spaces(message))
    reminder = Reminder()
    reminder.params = {"run_date": create_datetime(date__time_dict), "trigger":"date"}
    reminder.message = msg

    return reminder
