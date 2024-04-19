from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_text

# from bot.actions import get_reminder, add_reminder
# from bot.state_groups import MainDialog
# from utils.converter import conv_voice

add_reminder_router = Router()

@add_reminder_router.message(F.text | F.voice)
async def get_message_or_voice(message: Message):
    text = await  get_text(message)
    await message.answer(text)
