from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers import botControl
from loader import dp
from states.default import StateDefault
from utils.db_api import db_commands
from utils.values import menu_values, values_title


@dp.message_handler(state=StateDefault.review, content_types=types.ContentType.ANY)
async def message_review(message: types.Message, state: FSMContext):
    text = message.text
    user = await db_commands.get_user(user_id=message.from_user.id,
                                      full_name=message.from_user.full_name,
                                      username=message.from_user.username)
    user_lang = user.language
    if text in menu_values.BACK_BUTTON.values():
        await botControl.home_state(message=message, language=user_lang, reset=True)
    else:
        await state.update_data(category_review=text)
        await botControl.review_text(language=user_lang, message=message)


@dp.message_handler(state=StateDefault.review_text, content_types=types.ContentType.ANY)
async def message_review_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category_review = data.get('category_review') if data.get('category_review') else ''
    text = message.text
    user = await db_commands.get_user(user_id=message.from_user.id,
                                      full_name=message.from_user.full_name,
                                      username=message.from_user.username)
    user_lang = user.language
    if text in menu_values.BACK_BUTTON.values():
        await botControl.home_state(message=message, language=user_lang, reset=True)
    else:
        if category_review:
            category_review = f'Категория отзыва: <b>{category_review}</b>'
            await botControl.forward_to_channels(user=user, message=message, send_client=False, text=category_review)
        await botControl.forward_to_channels(user=user, message=message)
        await message.answer(values_title.GOT_REVIEW[user_lang])
        if text:
            await db_commands.save_review(user=user, comment=text, category=category_review)
