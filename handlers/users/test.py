from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from utils.excel import excel_command

from django_project.telegrambot.usersmanage.models import User


@dp.message_handler(Command('test'), state='*')
async def message_han(message: types.Message):
    pass
