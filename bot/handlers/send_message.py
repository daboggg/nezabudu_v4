import json
import time
from datetime import datetime, timedelta

from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import as_list, Italic, Bold

from bot.core import bot, scheduler
from bot.keyboards.delay_keyboard import delay_kb
from db.db_actions import get_auto_delay_time
from parser_v4.reminder import Reminder
from utils.from_datetime_to_str import datetime_to_short_str


# функция для отправки напоминаний
async def send_reminder(user_id: int,
                        reminder: Reminder,
                        run_time: datetime,
                        repeated_notification: int = 0,
                        **kwargs) -> None:
    auto_delay_time = await get_auto_delay_time(user_id)
    auto_delay_time = json.loads(auto_delay_time)

    # форматирование текста для напоминания
    format_text = as_list(
        # Bold(datetime_to_short_str(run_time)),
        Bold(reminder.period if reminder.period else datetime_to_short_str(run_time)),
        Italic(f'повторное оповещение: {repeated_notification}' if repeated_notification else ''),
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{reminder.message}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )

    remind_id = str(time.time_ns())

    # если оповещение повторное, удалить предыдущее сообщение
    if msg := kwargs.get("message", None):
        try:
            await msg.delete()
        except TelegramBadRequest:
            pass

    message = await bot.send_message(user_id, format_text.as_html(), reply_markup=await delay_kb(remind_id, user_id))

    # добавить задание на повторное оповещения
    scheduler.add_job(
        send_reminder,
        run_date=datetime.now() + timedelta(**auto_delay_time),
        id=remind_id,
        trigger='date',
        name=str(user_id),
        kwargs={
            'user_id': user_id,
            'reminder': reminder,
            'run_time': run_time,
            'repeated_notification': repeated_notification + 1,
            'message': message
        },
    )
