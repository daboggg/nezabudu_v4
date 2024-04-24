import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold, Italic
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Back, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import AdminSG
from db.db_actions import all_reminder_completed, get_users_from_db, get_user_from_db
from models import User


async def get_general_statistics(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    return {
        'all_jobs': len(apscheduler.get_jobs(jobstore='sqlite')),
        'all_reminder_completed': await all_reminder_completed()
    }


async def get_users(dialog_manager: DialogManager, **kwargs) -> dict[str, list]:
    users_from_db: list[User] = await get_users_from_db()
    users = [(user.first_name, user.last_name, user.id) for user in users_from_db]
    return {
        'users': users,
    }


async def get_user(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    user_id = dialog_manager.dialog_data.get("user_id")
    print(user_id)
    user: User = await get_user_from_db(int(user_id))
    return {
        'scheduled_reminders': len(list(filter(lambda j: j.name == str(user.id), apscheduler.get_jobs()))),
        'reminder_completed': user.reminder_completed,
        'user': f'{user.first_name} {user.last_name}'
    }


async def on_user_selected(callback: CallbackQuery, widget: Any,
                           manager: DialogManager, user_id: str) -> None:
    manager.dialog_data["user_id"] = user_id
    await manager.switch_to(AdminSG.show_user_statistics)


admin_dialog = Dialog(
    Window(
        Const(Bold("⚙️ выберите раздел").as_html()),
        Column(
            SwitchTo(Const("общая статистика"), state=AdminSG.general_statistics, id="general_statistics"),
            SwitchTo(Const("статистика по пользователям"), state=AdminSG.users_statistics,
                     id="users_statistics"),
        ),
        state=AdminSG.select_statistics
    ),
    Window(
        Const(Bold("Общая статистика:\n").as_html()),
        Format(Italic("Всего напоминаний: {all_jobs}").as_html()),
        Format(Italic("Всего выполненных напоминаний: {all_reminder_completed}").as_html()),
        Back(Const("назад")),
        getter=get_general_statistics,
        state=AdminSG.general_statistics
    ),
    Window(
        Const(Bold("Статистика по пользователям:\n").as_html()),
        ScrollingGroup(
            Select(
                Format("{item[0]} {item[1]}"),
                id="s_users",
                item_id_getter=operator.itemgetter(2),
                items="users",
                on_click=on_user_selected,
            ),
            id='scroll',
            width=1,
            height=7
        ),
        # Back(Const("назад")),
        SwitchTo(Const("назад"), state=AdminSG.select_statistics, id='back2'),
        state=AdminSG.users_statistics,
        getter=get_users,
    ),
    Window(
        Format(Bold("Статистика по пользователю {user}:\n").as_html()),
        Format(Italic("Запланированных напоминаний: {scheduled_reminders}").as_html()),
        Format(Italic("Выполненных напоминаний: {reminder_completed}").as_html()),
        Back(Const("назад")),
        state=AdminSG.show_user_statistics,
        getter=get_user

    )
)
