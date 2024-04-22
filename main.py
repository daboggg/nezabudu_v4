import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.comands import set_commands
from bot.core import bot, scheduler
from bot.dialogs.list_reminders_dialog import list_reminders_dialog
from bot.dialogs.settings_dialog import setup_dialog
from bot.handlers.add_reminder_handlers import add_reminder_router
from bot.handlers.cmd import cmd_router
from bot.handlers.delay_remind_hahdlers import delay_remind_router
from bot.handlers.delete_reminder_handlers import cancel_reminder_router
from bot.handlers.edit_reminder_handlers import edit_reminder_router
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from settings import settings


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')



async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')
    scheduler.shutdown()


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger(__name__)

    #запускаю скедулер
    scheduler.start()


    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # подключение роутеров
    dp.include_routers(
        cmd_router,
        delay_remind_router,
        edit_reminder_router,
        add_reminder_router,
        cancel_reminder_router,
        list_reminders_dialog,
        setup_dialog,
    )

    # подключение диалогов
    setup_dialogs(dp)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info('start')


    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
