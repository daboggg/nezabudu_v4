from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder


add_reminder_router = Router()

@add_reminder_router.message(F.text | F.voice)
async def get_message_or_voice(message: Message, apscheduler: AsyncIOScheduler):
    try:
        reminder = await  get_reminder(message)
        if reminder.message:
            add_reminder(message, apscheduler, reminder)
            await message.answer('установл')
        else:
            # get_text(reminder)
            pass
    except Exception as e:
        print(str(e))
    # await message.answer(reminder)
