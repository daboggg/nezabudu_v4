from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.send_message import send_reminder
from parser_v4.parse import parse
from parser_v4.reminder import Reminder
from utils.converter import conv_voice


# получить reminder из message
async def get_reminder(message: Message):
    if message.text:
        return parse(message.text)
    else:
        return parse(await conv_voice(message, message.bot))


# добавляет reminder в скедулер
def add_reminder (message: Message, apscheduler: AsyncIOScheduler, reminder: Reminder):
    apscheduler.add_job(send_reminder,
                        kwargs={
                            'user_id': message.from_user.id,
                            'reminder': reminder,
                        },
                        jobstore='sqlite',
                        **reminder.params)