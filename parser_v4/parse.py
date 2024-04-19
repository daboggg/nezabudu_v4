import logging
import re

from parser_v4 import every, in_date,through
from parser_v4.data import every_data
from parser_v4.reminder import Reminder

logger = logging.getLogger(__name__)

def parse(reminder_str: str) -> Reminder:
    # удалить в конце строки точку
    if reminder_str.endswith("."): reminder_str = reminder_str[:-1]

    # если в составе строки есть слово "через" или его варианты
    if "через" in reminder_str or "Через" in reminder_str:
        # удалить слово "Через" или "через" из строки
        reminder_str = re.sub("Через|через", "", reminder_str)
        result = through.start(reminder_str)
        logger.info(f"возвращенное из парсера значение: {result}")
        return result

    # если в составе строки есть слово "каждый" или его варианты
    elif set(every_data).intersection(reminder_str.split(" ")):
        # удалить слово "каждый" или его варианты
        reminder_str = re.sub("|".join(every_data), "", reminder_str)
        result = every.start(reminder_str)
        logger.info(f"возвращенное из парсера значение: {result}")
        return result

    else:
        result = in_date.start(reminder_str)
        logger.info(f"возвращенное из парсера значение: {result}")
        return result

if __name__ == '__main__':
    print(parse("все равно через 8    Лет    7    Дней     никого не поймают 8 Минут."))
    # parse("все равно через 8    Лет,    7    Дней,  и   3 часа,     никого не поймают.")
    # start("Каждый      уебищный     31     День     в   23.02    что    то    происходит")
    # parse("Каждый уебищный  09        Числа     в  12.45   что то происходит")
    # start("Каждый    уебищный  09        Среда   в  12.45   что то происходит")
    # start("тропики     в    африке   1    Января   в    1:44    и    где    то      там")
    # start("тропики     в    африке   Среда   в    1:44    и    где    то      там")
    # start("тропики     в    африке   12.12.24   в    1:44    и    где    то      там")
    # start("тропики     в    африке      в    15:03    и    где    то      там")
    # print(parse("17 декабря в 18.00"))
