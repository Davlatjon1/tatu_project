from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from data.config import SEND_FILE_ITEMS, MAIN_LANGUAGE_INLINE_MODE, SEND_ALL_PRODUCTS, SEND_ALL_PRODUCTS_TEXT
from handlers import botControl
from loader import dp
from utils.db_api import db_commands
from utils.misc import rate_limit


# @rate_limit(300, 'all_items')
# @dp.message_handler(Command("all_items"), state='*')
async def price_list(message: types.Message, state: FSMContext):
    if SEND_FILE_ITEMS:
        await botControl.send_file_items(message=message, language=MAIN_LANGUAGE_INLINE_MODE)
        return
    if SEND_ALL_PRODUCTS_TEXT:
        await botControl.send_all_product_text(message=message, language=MAIN_LANGUAGE_INLINE_MODE)
        return
    if SEND_ALL_PRODUCTS:
        user = await db_commands.get_user(user_id=message.from_user.id,
                                          full_name=message.from_user.full_name,
                                          username=message.from_user.username)
        await botControl.send_all_product(user=user, message=message)
