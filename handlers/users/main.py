import datetime
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import SEND_ALL_PRODUCTS, SEND_FILE_ITEMS
from handlers import botControl, botControlOrder, act_sverki_state
from handlers.users import all_items
from loader import dp
from states.default import StateDefault
from utils.db_api.db_commands import get_user
from utils.misc import rate_limit
from utils.values import menu_values, others, values_title
from keyboards.default import keyboards as kb


# @rate_limit(20, 'all_items')
@dp.message_handler(lambda message: message.text in menu_values.PRODUCTS.values(), state=StateDefault.main)
async def message_main(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    await botControl.after_product(user_lang, message, all_product=SEND_ALL_PRODUCTS, user=user)
    message_search = await botControl.search(language=user_lang, message=message)
    await state.update_data(basket_message=[message_search])


@rate_limit(300, "all_items")
@dp.message_handler(lambda message: message.text in menu_values.PRICE_LIST.values(), state=StateDefault.main)
@dp.message_handler(Command("all_items"), state="*")
async def message_price_list(message: types.Message, state: FSMContext):
    await all_items.price_list(message=message, state=state)


# @rate_limit(20, 'all_items_no_pictures')
@dp.message_handler(lambda message: message.text in menu_values.PRODUCTS_WITHOUT_PICTURE.values(),
                    state=StateDefault.main)
async def message_main(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    await botControl.after_product(user_lang, message, all_product=True, user=user, photo_or_video=False)
    message_search = await botControl.search(language=user_lang, message=message)
    await state.update_data(basket_message=[message_search])


# --------------------------------------- MAIN --------------------------------------
@dp.message_handler(state=StateDefault.main)
async def message_main(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    if text in menu_values.CHANGE_LANGUAGE.values():
        has_changed_lang = await botControl.change_language(user_id=user_id, user_lang=user_lang, user=user)
        markup = await kb.main_keyboards(has_changed_lang)
        await botControl.choose_below(language=has_changed_lang, message=message, markup=markup)
    elif text in menu_values.PRODUCTS.values():
        await botControl.after_product(user_lang, message, all_product=True, user=user)
        message_search = await botControl.search(language=user_lang, message=message)
        await state.update_data(basket_message=[message_search])
    elif text in menu_values.BASKET.values():
        await botControl.after_basket(message=message, language=user_lang, user=user)
        await botControl.search(language=user_lang, message=message)
    elif text in menu_values.ABOUT_US.values():
        await botControl.about_us(message=message, language=user_lang)
    elif text in menu_values.REVIEW.values():
        await botControl.review(language=user_lang, message=message)
    elif text in menu_values.MY_ORDERS.values():
        await botControlOrder.my_orders(message=message, user=user)
        await botControl.search(language=user_lang, message=message)
    elif text in menu_values.ACT_OF_RECONCILIATION.values():
        if user.access_act_sverki:
            await botControl.act_sverki(user=user, message=message)
        else:
            await botControl.not_allowed_to_act_sverki(user=user, message=message)
    # elif text in menu_values.PRICE_LIST.values():
    #     await botControl.send_file_items(message=message, language=user_lang)
    else:
        markup = await kb.main_keyboards(language=user_lang)
        await botControl.choose_below(language=user_lang, message=message, markup=markup)


# --------------------------------------- CATEGORY --------------------------------------
@dp.message_handler(state=StateDefault.category, content_types=types.ContentType.TEXT)
async def message_category(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    categories = await menu_values.get_categories(language=user_lang)
    if text in categories:
        await botControl.after_category(category=text, message=message, language=user_lang)
        await state.update_data(category=text)  # save, which category user clicked
    elif text in menu_values.BASKET.values():
        await botControl.after_basket(message=message, language=user_lang, user=user)
    elif text in menu_values.BACK_BUTTON.values() or text in menu_values.HOME_BUTTON.values():
        await botControl.home_state(language=user_lang, message=message)
    else:  # always updated categories, because user would be updated on Django (c) Davik
        markup = await kb.category_keyboards(language=user_lang, categories=categories)
        await botControl.choose_category(language=user_lang, message=message, markup=markup)


# --------------------------------------- SUBCATEGORY --------------------------------------
@dp.message_handler(state=StateDefault.subcategory, content_types=types.ContentType.TEXT)
async def message_subcategory_or_item(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    data = await state.get_data()
    category = data.get("category")
    res_sub_or_items = await menu_values.get_subcategories_or_items_by_category(language=user_lang,
                                                                                category=category)
    sub_or_items = res_sub_or_items.get(others.SUBCATEGORIES_OR_ITEMS)
    if text in sub_or_items:
        items = res_sub_or_items.get(others.ITEMS_CATEGORY)
        subcategories = res_sub_or_items.get(others.SUBCATEGORIES)
        if text in items:
            await botControl.after_item(item_name=text, message=message, user=user)
            await state.update_data(item=text)
        elif text in subcategories:
            subcategory = text
            await botControl.after_subcategory(message=message, language=user_lang, category=category,
                                               subcategory=subcategory)
            await state.update_data(subcategory=text)
    elif text in menu_values.BASKET.values():
        await botControl.after_basket(message=message, language=user_lang, user=user)
    elif text in menu_values.BACK_BUTTON.values():
        await botControl.after_product(language=user_lang, message=message)
    elif text in menu_values.HOME_BUTTON.values():
        await botControl.home_state(language=user_lang, message=message)
    else:
        await botControl.after_category(category=category, message=message, language=user_lang)


# --------------------------------------- ITEM --------------------------------------
@dp.message_handler(state=StateDefault.item, content_types=types.ContentType.TEXT)
async def message_items(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")
    res_sub_or_items = await menu_values.get_subcategories_or_items_by_category(language=user_lang,
                                                                                category=category,
                                                                                subcategory=subcategory)
    items = res_sub_or_items.get(others.ITEMS_FULL)
    if text in items:
        await botControl.after_item(item_name=text, message=message, user=user)
        await state.update_data(item=text)
    elif text in menu_values.BASKET.values():
        await botControl.after_basket(message=message, language=user_lang, user=user)
    elif text in menu_values.BACK_BUTTON.values():
        await botControl.after_category(language=user_lang, message=message, category=category)
    elif text in menu_values.HOME_BUTTON.values():
        await botControl.home_state(language=user_lang, message=message)
    else:
        markup = await kb.sub_or_item_keyboards_by_category(language=user_lang, category='',
                                                            sub_or_items=items, which='')
        await botControl.choose_product(language=user_lang, message=message, markup=markup)


@dp.message_handler(state=StateDefault.act_sverki, content_types=types.ContentTypes.ANY)
async def message_period(message: types.Message, state: FSMContext):
    text = message.text
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    today = datetime.date.today()
    end_period = today.strftime('%d.%m.%Y')
    if text in values_title.DAY.values():
        start_period = end_period
        await act_sverki_state.act_sverki_text(start_period=start_period, end_period=end_period, user=user,
                                               message=message)
    elif text in values_title.WEEK.values():
        start_period = (today - datetime.timedelta(days=7)).strftime('%d.%m.%Y')
        await act_sverki_state.act_sverki_text(start_period=start_period, end_period=end_period, user=user,
                                               message=message)
    elif text in values_title.MONTH.values():
        start_period = (today - datetime.timedelta(days=31)).strftime('%d.%m.%Y')
        await act_sverki_state.act_sverki_text(start_period=start_period, end_period=end_period, user=user,
                                               message=message)
    elif text in menu_values.BACK_BUTTON.values():
        await botControl.home_state(language=user.language, message=message)
    elif isinstance(text, str):
        split_space = text.split()
        if not (re.match(r'[0-9]{1,2} [0-9]{2} [0-9]{4}[\n, ]+[0-9]{1,2} [0-9]{2} [0-9]{4}', text)
                and len(split_space) > 0 and len(split_space[-1]) == 4):
            await botControl.act_sverki(user=user, message=message)
            return

        try:
            start_period = datetime.datetime.strptime('.'.join(split_space[:3]), '%d.%m.%Y').strftime('%d.%m.%Y')
            end_period = datetime.datetime.strptime('.'.join(split_space[3:]), '%d.%m.%Y').strftime('%d.%m.%Y')
            await act_sverki_state.act_sverki_text(start_period=start_period, end_period=end_period, user=user,
                                                   message=message)
        except:
            await botControl.act_sverki(user=user, message=message)

    else:
        await botControl.act_sverki(user=user, message=message)
