class DatetimeValueException(Exception):
    pass


# перевод для ошибок
errors_translation = {
    "hour must be in 0..23": "час должен быть в диапазоне 0..23",
    "minute must be in 0..59": "минута должна быть в диапазоне 0..59",
    "month must be in 1..12": "месяц должен быть в диапазоне 1..12",
    "day is out of range for month": "день находится вне диапазона для месяца",
}
