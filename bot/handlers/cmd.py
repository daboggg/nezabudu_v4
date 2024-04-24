from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_marked_section, as_list, Italic
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import ListOfRemindersSG, SetupRemindersSG, AdminSG
from db.db_actions import add_user_to_db
from settings import settings

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await add_user_to_db(message.from_user.id, message.from_user.username, message.from_user.first_name,
                         message.from_user.last_name)
    await message.answer(Italic("✏️ 🎤 пожалуйста введите время и текст сообщения").as_html())


@cmd_router.message(Command(commands="help"))
async def cmd_start(message: Message) -> None:
    title = Bold("📌 Используйте примеры для установки напоминания.\n")
    examples = as_marked_section(
        Bold("Например:"),
        "через 20 минут",
        "через 1 месяц, 2 дня, 6 часов",
        "через 1 год 20 минут",
        "в среду в 18.00",
        "в пятницу"
        "в 13:30",
        "завтра в 23-36",
        "послезавтра в 23-36",
        "31 декабря в 22.17",
        "12.12.24 в 8.55",
        "каждый день 19-30",
        "каждую субботу в 13:14",
        "каждое 17 апреля",
        "каждое 14 число",
        "каждое 14 число в 12:12",
        "каждый последний день месяца",
        "каждый последний день месяца в 12.22",
        marker="✔️ "
    )
    help_text = as_list(title, examples)

    await message.answer(help_text.as_html())


@cmd_router.message(Command(commands="list"))
async def list_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListOfRemindersSG.start, mode=StartMode.RESET_STACK)


@cmd_router.message(Command(commands="setup"))
async def settings_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(SetupRemindersSG.select_setting, mode=StartMode.RESET_STACK)


@cmd_router.message(Command(commands="admin"))
async def admin_panel(_, dialog_manager: DialogManager) -> None:
    if dialog_manager.event.from_user.id == settings.bots.admin_id:
        await dialog_manager.start(AdminSG.select_statistics, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.event.answer("Этот раздел только для админа")