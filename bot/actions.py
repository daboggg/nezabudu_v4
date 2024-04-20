from datetime import datetime, timedelta

from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.send_message import send_reminder
from bot.keyboards.delete_or_edit_reminder_keyboard import cancel_or_edit_kb
from parser_v4.parse import parse
from parser_v4.reminder import Reminder
from text_responses.reminder_info import get_reminder_info
from utils.converter import conv_voice


# получить reminder из message
async def get_reminder(message: Message):
    if message.text:
        return parse(message.text)
    else:
        return parse(await conv_voice(message, message.bot))


# добавляет reminder в скедулер
async def add_reminder (message: Message, apscheduler: AsyncIOScheduler, reminder: Reminder):
    # добавить задание в скедулер
    job = apscheduler.add_job(send_reminder,
                        kwargs={
                            'user_id': message.from_user.id,
                            'reminder': reminder,
                        },
                        jobstore='sqlite',
                        **reminder.params)

    # текст задания
    reminder_info = get_reminder_info(reminder, job)

    # сообщение об установленном задании
    last_msg = await message.answer(reminder_info, reply_markup=cancel_or_edit_kb())

    # удалить клавиатуру через промежуток времени
    apscheduler.add_job(
        delete_keyboard,
        trigger='date',
        run_date = datetime.now() + timedelta(seconds=15),
        kwargs={
            'message': last_msg,
        }
    )

# удаление клавиатуры(Отменить, Изменить)
async def delete_keyboard(message: Message):
    await message.edit_reply_markup(reply_markup=None)
