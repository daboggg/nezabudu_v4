from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import as_list, Bold, as_key_value, Italic
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import RescheduleReminderSG
from utils.from_datetime_to_str import datetime_to_str, datetime_to_short_str

delay_remind_router = Router()


# отложить напоминание
# @delay_remind_router.callback_query(F.data.startswith("delay_remind"))
# async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
#     tmp = callback.data.split(":")
#     job_id = tmp[1]
#     res = {tmp[2]: int(tmp[3])}
#     job: Job = apscheduler.reschedule_job(job_id=job_id, trigger='date',
#                                           run_date=datetime.now() + timedelta(**res))
#     remind_info = as_list(
#         Bold("💡 Напоминание отложено.\n"),
#         as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
#         as_key_value("📝", Italic(job.kwargs.get("text"))),
#     ).as_html()
#
#     await callback.answer()
#     await callback.message.edit_text(remind_info)


# напоминание выполнено
@delay_remind_router.callback_query(F.data.startswith("done_remind"))
async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler) -> None:
    tmp = callback.data.split(":")
    job_id = tmp[1]

    job: Job = apscheduler.get_job(job_id)

    # форматирование текста для напоминания
    format_text = as_list(
        '✔️ Выполнено',
        '',
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{job.kwargs.get('reminder').message}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )

    await callback.answer()
    await callback.message.edit_text(format_text.as_html())
    job.remove()


# переназначить напоминание
@delay_remind_router.callback_query(F.data.startswith("reschedule_remind"))
async def reschedule_remind(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler) -> None:
    tmp = callback.data.split(":")
    job_id = tmp[1]
    job = apscheduler.get_job(job_id)
    reminder = job.kwargs.get('reminder')
    await state.update_data(reminder=reminder)
    job.remove()
    await callback.answer()
    await callback.message.edit_text(Italic("✏️ 🎤 введите время напоминания").as_html())
    await state.set_state(RescheduleReminderSG.reschedule_reminder)


@delay_remind_router.message(RescheduleReminderSG.reschedule_reminder, F.text | F.voice)
async def get_remind(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler) -> None:
    state_data = await state.get_data()
    old_reminder = state_data.get('reminder')

    try:
        new_reminder = await get_reminder(message)
        if not new_reminder.message:
            new_reminder.message = old_reminder.message
        await add_reminder(message, apscheduler, new_reminder, True)
        await state.clear()
    except Exception as e:
        await not_text_not_voice(message)


@delay_remind_router.message(RescheduleReminderSG.reschedule_reminder)
async def not_text_not_voice(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 введите время напоминания").as_html())
