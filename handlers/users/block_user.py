from aiogram import types
from data.config import MAIN_LANGUAGE_INLINE_MODE
from filters.filters import IsUserHasBlockMessage
from loader import dp
from utils.values import values_title


@dp.message_handler(IsUserHasBlockMessage(), state="*")
async def block_user_message(message: types.Message):
    await message.answer(values_title.NOT_ACCESS[MAIN_LANGUAGE_INLINE_MODE])


@dp.callback_query_handler(IsUserHasBlockMessage(), state="*")
async def block_user_callback(call: types.CallbackQuery):
    await call.answer(text=values_title.NOT_ACCESS[MAIN_LANGUAGE_INLINE_MODE], cache_time=5, show_alert=True)


@dp.inline_handler(IsUserHasBlockMessage(), state="*")
async def block_user_inline(query: types.InlineQuery):
    await query.answer(results=[
        types.InlineQueryResultArticle(
            id="unknown",
            title=values_title.NOT_ACCESS[MAIN_LANGUAGE_INLINE_MODE],
            input_message_content=types.InputTextMessageContent(
                message_text=values_title.NOT_ACCESS[MAIN_LANGUAGE_INLINE_MODE],
            ),
        )
    ],
        cache_time=5)
