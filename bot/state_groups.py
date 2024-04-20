from aiogram.fsm.state import StatesGroup, State


class AddReminderSG(StatesGroup):
    get_text = State()

class EditReminderSG(StatesGroup):
    get_message = State()