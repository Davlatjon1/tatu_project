from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('get_id'), state='*')
async def message_handler(message: types.Message):
    reply_to_message = message.reply_to_message
    if not reply_to_message:
        return
    if reply_to_message.photo:
        photos = reply_to_message.photo
        await message.answer(text=photos[-1].file_id)
    elif reply_to_message.voice:
        voice = reply_to_message.voice
        await message.answer(text=voice.file_id)
    elif reply_to_message.video:
        video = reply_to_message.video
        await message.answer(text=video.file_id)
    elif reply_to_message.document:
        document = reply_to_message.document
        await message.answer(text=document.file_id)
    elif reply_to_message.location:
        location = reply_to_message.location
        await message.answer(f"Latitude: {location.latitude}\nLongitude: {location.longitude}")
    else:
        await message.answer(reply_to_message.message_id)