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


class SetupRemindersSG(StatesGroup):
    select_setting = State()
    select_auto_delay = State()
    select_buttons_delay = State()

class AdminSG(StatesGroup):
    select_statistics = State()
    general_statistics = State()
    users_statistics = State()
    show_user_statistics = State()
