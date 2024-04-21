from datetime import datetime

months = ["", "января", "февраля", "марта", "апреля",
          "мая", "июня", "июля", "августа", "сентября",
          "октября", "ноября", "декабря", ]

day_of_week = ["в понедельник", "во вторник", "в среду", "в четверг",
               "в пятницу", "в субботу", "в воскресенье", ]


def datetime_to_str(date: datetime):
    hour = date.hour
    minute = date.minute
    if hour < 10:
        hour = f'0{hour}'
    if minute <10:
        minute = f'0{minute}'
    return f"{date.day} {months[date.month]} {date.year} г. ({day_of_week[date.weekday()]}) в {hour}:{minute}"


def datetime_to_short_str(date: datetime):
    hour = date.hour
    minute = date.minute
    if hour < 10:
        hour = f'0{hour}'
    if minute <10:
        minute = f'0{minute}'
    return f"{date.day} {months[date.month]}  в {hour}:{minute}"