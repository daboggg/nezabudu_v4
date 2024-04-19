from aiogram import Bot

from settings import settings

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')