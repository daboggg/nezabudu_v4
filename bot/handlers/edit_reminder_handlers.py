from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Italic
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import EditReminderSG
from parser_v4.reminder import Reminder
from utils.converter import conv_voice

edit_reminder_router = Router()


# обработка отклика на кнопку "Изменить"
@edit_reminder_router.callback_query(F.data.startswith("edit_remind"))
async def start_edit_reminder(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler) -> None:
    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]
    apscheduler.remove_job(hide_kb_id)
    job = apscheduler.get_job(job_id)

    await callback.answer()
    await state.update_data(job=job)
    await callback.message.edit_text(f"👉 {job.kwargs.get('reminder').message}")
    await callback.message.answer(Italic("✏️ 🎤 введите время и текст напоминания").as_html())
    await state.set_state(EditReminderSG.get_message)


# Обработка текста или голоса для изменения напоминания
@edit_reminder_router.message(EditReminderSG.get_message, F.text | F.voice)
async def get_text_or_voice(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler) -> None:
    state_data = await state.get_data()
    job: Job = state_data.get('job')
    old_reminder: Reminder = job.kwargs.get('reminder')
    try:
        new_reminder = await get_reminder(message)
        if not new_reminder.message:
            new_reminder.message = old_reminder.message
        await add_reminder(message, apscheduler, new_reminder, True)
    except Exception as e:
        if message.text:
            old_reminder.message = message.text
        elif message.voice:
            old_reminder.message = await conv_voice(message, message.bot)
        await add_reminder(message, apscheduler, old_reminder, True)
    finally:
        job.remove()
        await state.clear()


# Обработка если пришел не текст и не голос
@edit_reminder_router.message(EditReminderSG.get_message)
async def other_msg(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 введите время напоминания").as_html())
