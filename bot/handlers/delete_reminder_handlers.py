from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold, Strikethrough
from apscheduler.schedulers.asyncio import AsyncIOScheduler

cancel_reminder_router = Router()

# отмена напоминания
@cancel_reminder_router.callback_query(F.data.startswith("cancel_remind"))
async def cancel_reminder(callback: CallbackQuery, apscheduler: AsyncIOScheduler)->None:
    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]
    apscheduler.remove_job(hide_kb_id)
    apscheduler.remove_job(job_id)
    await callback.answer()

    part_msg = callback.message.text.split("\n")
    msg = Bold(f"{part_msg[0].replace('запланировано', 'отменено')}\n").as_html() + Strikethrough(
        '\n'.join(part_msg[1:])).as_html()

    await callback.message.edit_text(msg)
