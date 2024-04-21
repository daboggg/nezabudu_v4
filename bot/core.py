from aiogram import Bot
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import settings

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

scheduler = AsyncIOScheduler(timezone="Europe/Moscow", jobstores={'sqlite': SQLAlchemyJobStore(url=settings.db.db_url)})