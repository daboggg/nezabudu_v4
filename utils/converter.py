from aiogram import Bot
from aiogram.types import Message

import soundfile as sf
import speech_recognition as sr


async def conv_voice(message: Message, bot: Bot):
    await bot.download(message.voice, "tmp.ogg")

    data, samplerate = sf.read('tmp.ogg')
    sf.write('out.wav', data, samplerate)

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.3
    with sr.AudioFile('out.wav') as source:
        audio = recognizer.record(source)

    return recognizer.recognize_google(audio, language='ru-RU')
