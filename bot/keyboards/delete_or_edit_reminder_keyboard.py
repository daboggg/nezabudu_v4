from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_or_edit_kb(job_id: str, hide_kb_id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text=f'✖️ Отменить', callback_data=f'cancel_remind:{job_id}:{hide_kb_id}')
    ikb.button(text=f'⚙ Изменить', callback_data=f'edit_remind:{job_id}:{hide_kb_id}')

    return ikb.adjust(2).as_markup()
