import ast
import json

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_actions import get_delay_times


async def delay_kb(job_id: str, user_id: int) -> InlineKeyboardMarkup:
    delay_times = await get_delay_times(user_id)
    # из строки в список
    delay_times = json.loads(delay_times)
    # из строк внутри списка в кортежи внутри списка
    delay_times = [ast.literal_eval(t) for t in delay_times]
    # сортировка
    delay_times = sorted(delay_times, key=lambda x: (-(ord(x[0][0])), x[1]))

    ikb = InlineKeyboardBuilder()

    for time in delay_times:
        ikb.button(text=f'+{time[2]}', callback_data=f'delay_remind:{job_id}:{time[0]}:{time[1]}')

    ikb.button(text=f'⏰ Установить', callback_data=f'reschedule_remind:{job_id}')
    ikb.button(text=f'✔️ Выполнено', callback_data=f'done_remind:{job_id}')

    return ikb.adjust(3).as_markup()
