from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold
from apscheduler.job import Job

from parser_v4.reminder import Reminder
from utils.from_datetime_to_str import datetime_to_str


# форматированный текст запланированного или перепланированного напоминания
def get_reminder_info(reminder: Reminder, job: Job, edited: bool = False) -> str:
    item = []
    if rd := reminder.period:
        item.append(as_key_value("♾", Italic(rd)))
    reminder_info = as_list(
        Bold("💡 Напоминание перепланировано.\n") if edited else Bold("💡 Напоминание запланировано.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(reminder.message)),

    ).as_html()
    return reminder_info

# async def edit_reminder_info(state: FSMContext, job: Job):
#     state_data = await state.get_data()
#     reminder: Reminder = state_data.get("reminder")
#     message = job.kwargs.get("text")
#     period = reminder.period
#     item = []
#     if rd := period:
#         item.append(as_key_value("♾", Italic(rd)))
#     reminder_info = as_list(
#         Bold("💡 Напоминание запланировано.\n"),
#         as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
#         *item,
#         as_key_value("📝", Italic(message)),
#
#     ).as_html()
#     return reminder_info
