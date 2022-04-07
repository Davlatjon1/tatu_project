from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers import botControl
from loader import dp
from states.default import StateDefault
from utils.db_api import db_commands as commands


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    user = await commands.get_user(user_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username)
    user_lang = user.language
    await botControl.main_menu(language=user_lang, message=message)
    await botControl.reset_data_user()


@dp.message_handler(Command("search"), state='*')
async def search(message: types.Message):
    user = await commands.get_user(user_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username)
    user_lang = user.language
    await botControl.search(user_lang, message)
