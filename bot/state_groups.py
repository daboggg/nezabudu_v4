from aiogram.fsm.state import StatesGroup, State


class AddReminderSG(StatesGroup):
    get_text = State()

class EditReminderSG(StatesGroup):
    get_message = State()

class RescheduleReminderSG(StatesGroup):
    reschedule_reminder = State()

class ListOfRemindersSG(StatesGroup):
    start = State()
    show_reminder = State()