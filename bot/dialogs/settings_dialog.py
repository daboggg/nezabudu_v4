import json
import operator

from aiogram.types import Message
from aiogram.utils.formatting import Bold
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import Radio, ManagedRadio, SwitchTo, Column, Multiselect, Group, \
    ManagedMultiselect
from aiogram_dialog.widgets.text import Format, Const

from bot.state_groups import SetupRemindersSG
from db.db_actions import set_auto_delay_time, get_auto_delay_time, set_delay_times, get_delay_times


async def get_data(**kwargs):
    intervals = [
        ("minutes", 5, "5 мин"),
        ("minutes", 10, "10 мин"),
        ("minutes", 15, "15 мин"),
        ("minutes", 30, "30 мин"),
        ("hours", 1, "1 час"),
        ("hours", 2, "2 часа"),
        ("hours", 3, "3 часа"),
        ("hours", 6, "6 часов"),
        ("days", 1, "1 день"),
        ("days", 2, "2 дня"),
        ("days", 3, "3 дня"),
        ("days", 7, "7 дней"),
    ]
    return {
        "intervals": intervals,
    }


async def on_state_changed_auto_delay(event: Message, select: ManagedRadio, dialog_manager: DialogManager, data):
    await set_auto_delay_time(event.from_user.id, {"minutes": int(data)})


async def on_state_changed_delay(event: Message, select: ManagedRadio, dialog_manager: DialogManager, data):
    await set_delay_times(event.from_user.id, json.dumps(select.get_checked(), ensure_ascii=False))


async def dialog_on_start(_, manager: ManagerImpl):
    res = await get_auto_delay_time(manager.event.from_user.id)
    auto_delay_time: dict = json.loads(res)

    res = await get_delay_times(manager.event.from_user.id)
    delay_times: list = json.loads(res)

    radio: ManagedRadio = manager.find('a_delay')
    multiselect: ManagedMultiselect = manager.find("btn_delay")

    await radio.set_checked(auto_delay_time.get("minutes"))
    if delay_times:
        for delay_time in delay_times:
            await multiselect.set_checked(delay_time, checked=True)


setup_dialog = Dialog(
    Window(
        Const(Bold("⚙️ выберите раздел").as_html()),
        Column(
            SwitchTo(Const("автоматическое откладывание"), state=SetupRemindersSG.select_auto_delay, id="auto_delay"),
            SwitchTo(Const("кнопки откладывания"), state=SetupRemindersSG.select_buttons_delay, id="button_delay"),
        ),
        state=SetupRemindersSG.select_setting
    ),
    Window(
        Const(Bold("⏰ Установите время, на которое напоминания будут автоматически откладываться.").as_html()),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="a_delay",
                item_id_getter=operator.itemgetter(1),
                items=[("5 минут", 5), ("10 минут", 10), ("15 минут", 15), ("20 минут", 20)],
                on_state_changed=on_state_changed_auto_delay
            ),
            SwitchTo(Const("назад"), state=SetupRemindersSG.select_setting, id='back1')
        ),
        getter=get_data,
        state=SetupRemindersSG.select_auto_delay
    ),
    Window(
        Const(Bold("Выберите кнопки откладывания напоминания").as_html()),
        Group(
            Multiselect(
                Format("🚩{item[2]}"),
                Format("{item[2]}"),
                id="btn_delay",
                item_id_getter=lambda x: x,
                # item_id_getter=operator.itemgetter(1),
                items="intervals",
                on_state_changed=on_state_changed_delay,
            ),
            width=3
        ),
        SwitchTo(Const("назад"), state=SetupRemindersSG.select_setting, id='back2'),
        getter=get_data,
        state=SetupRemindersSG.select_buttons_delay
    ),
    on_start=dialog_on_start
)
