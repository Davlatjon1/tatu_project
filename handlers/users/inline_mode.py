import logging
from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext
from django.db.models import Q

from data.config import MAIN_LANGUAGE_INLINE_MODE
from django_project.telegrambot.usersmanage.models import Item
from filters import AfterMode_ViaBot
from handlers import botControl, state_data, botControlOrder
from loader import dp
from utils.db_api import db_commands
from utils.values import values_title
from utils.values.others import get_attribute_by_language


@dp.message_handler(AfterMode_ViaBot(), state="*")
async def after_mode(message: types.Message, state: FSMContext):
    user = await db_commands.get_user(user_id=message.from_user.id,
                                      full_name=message.from_user.full_name,
                                      username=message.from_user.username)
    text = message.text
    attr = get_attribute_by_language(MAIN_LANGUAGE_INLINE_MODE)
    item = await db_commands.get_item_filter(first=True, show_bot=True,
                                             **{f"{attr}__icontains": text})

    if item:
        structure_add_order = await state_data.get_structure_from_more_order()
        if structure_add_order.get('access'):
            if botControlOrder.not_available_to_the_add_order(item):
                await message.answer(
                    text=values_title.not_allow_to_add_order(item_name=item.name, language=user.language))
                return
        await botControl.send_item(item=item, user=user, message=message, photo_or_video=True)
        await botControl.search(language=user.language, message=message)
    else:
        await message.answer(values_title.NOT_FOUND_ITEM[MAIN_LANGUAGE_INLINE_MODE])


@dp.inline_handler(lambda query: len(query.query) <= 2, state="*")
async def write_more(query: types.InlineQuery):
    await query.answer(results=[
        types.InlineQueryResultArticle(
            id="write_more",
            title=values_title.WRITE_MORE_INLINE[MAIN_LANGUAGE_INLINE_MODE],
            input_message_content=types.InputTextMessageContent(
                message_text=values_title.WRITE_MORE_INLINE[MAIN_LANGUAGE_INLINE_MODE],
            ),
        )
    ],
        cache_time=5)


@dp.inline_handler(lambda query: len(query.query) > 2, state="*")
async def search_items(query: types.InlineQuery):
    user = await db_commands.get_user(user_id=query.from_user.id,
                                      full_name=query.from_user.full_name,
                                      username=query.from_user.username)
    user_lang = user.language
    text = query.query

    offset = int(query.offset) if query.offset else 0

    list_text = text.split()
    items = Item.objects.filter(show_bot=True, category__show_bot=True)

    attr = get_attribute_by_language(language=user_lang)

    for search_text in list_text:
        items = items.filter(Q(**{f"{attr}__icontains": search_text}))
    try:
        items = items[offset:offset + 10].all()
    except Exception as err:
        logging.info(err)
        return

    if len(items) == 0:
        await query.answer(results=[
            types.InlineQueryResultArticle(
                id="not_found",
                title=values_title.NOT_FOUND_ITEM[MAIN_LANGUAGE_INLINE_MODE],
                input_message_content=types.InputTextMessageContent(
                    message_text=values_title.NOT_FOUND_ITEM[MAIN_LANGUAGE_INLINE_MODE],
                ),
            )
        ],
            cache_time=5)
        return

    results = []
    m_next_offset = str(offset + 10) if len(items) == 10 else ''
    i = 0
    for item in items:
        results.append(types.InlineQueryResultArticle(
            id=str(item.id),
            title=item.name,
            thumb_url=await get_link_aiograph(item),
            # description=f"{values_title.get_remainder(language=user_lang, num=item.reminder, tag=False)} {getattr(item, get_attribute_by_language(user_lang, name_object='description'))}",
            description=f"{values_title.get_remainder(language=user_lang, num=item.reminder, tag=False)}, {values_title.get_amount(num=item.price, language=user_lang, tag=False).lower()}; {values_title.get_desc_of_good(language=user_lang, item=item)}",
            input_message_content=types.InputTextMessageContent(
                message_text=getattr(item, attr),
                parse_mode="HTML"
            ),
        ))
        i = i + 1
    await query.answer(results=results, cache_time=1, next_offset=m_next_offset)


async def get_link_aiograph(item: Item):
    result = ''
    # if item.image_url_file_id:
    #     try:
    #         file = await dp.bot.get_file(item.image_url_file_id)
    #         url = file.get_url()
    #         result = url
    #     except Exception as err:
    #         item.image_url_file_id = ''
    #         item.save()
    #
    # if item.image.name:
    #     pass
    #     path = PATH_MEDIA
    #     file = types.InputFile(path_or_bytesio=path + item.image.name)
    #     form = aiohttp.FormData()
    #     form.add_field(name='file', value=file)
    #     async with dp.bot.session.post('https://telegra.ph/upload', data=form) as response:
    #         img_src = await response.json()
    #
    #     link = 'http://telegra.ph/' + img_src[0]["src"]
    #     result = link

    return result
