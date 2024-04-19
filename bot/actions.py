from aiogram.types import Message

from utils.converter import conv_voice


async def get_text(message: Message):
    if message.text:
        return message.text
    else:
        return await conv_voice(message, message.bot)