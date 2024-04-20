import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import AddReminderSG
from utils.converter import conv_voice

logger = logging.getLogger(__name__)

add_reminder_router = Router()

# добавляем текст к напоминанию
@add_reminder_router.message(AddReminderSG.get_text, F.text | F.voice)
async def get_text(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext) -> None:
    state_data = await state.get_data()
    reminder = state_data.get("reminder")
    if message.text:
        reminder.message = message.text
    elif message.voice:
        text = await conv_voice(message, message.bot)
        reminder.message = text
    await add_reminder(message, apscheduler, reminder)
    await state.clear()


# выполняется если не текст и не голос при добавлении текста к сообщению
@add_reminder_router.message(AddReminderSG.get_text)
async def other_text(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 введите текст напоминания").as_html())

# получение текста или голоса для reminder
@add_reminder_router.message(F.text | F.voice)
async def get_message_or_voice(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext)-> None:
    try:
        reminder = await  get_reminder(message)
        await state.update_data(reminder=reminder)
        if reminder.message:
            await add_reminder(message, apscheduler, reminder)
        else:
            await state.set_state(AddReminderSG.get_text)
            await message.answer(Italic("✏️ 🎤 введите текст напоминания").as_html())
    except Exception as e:
        logger.error(e)
        await other_msg(message)


# выполняется если не текст и не голос
@add_reminder_router.message()
async def other_msg(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 пожалуйста введите время и текст сообщения").as_html())
