from bot.create_bot import bot
from parser_v4.reminder import Reminder


# функция для отправки напоминаний
async def send_reminder( user_id: int, reminder: Reminder):
    await bot.send_message(user_id, reminder.message)