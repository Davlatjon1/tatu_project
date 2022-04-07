from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown as md
from django_project.telegrambot.usersmanage.models import BasketItem
from filters.filters import AddToBasket
from handlers import botControl, botControlOrder, state_data
from keyboards.default import keyboards as kb
from keyboards.inline import inlines
from keyboards.inline.callback_datas import buy_callback, edit_item_callback
from states.default import StateDefault, StateOrder
from loader import dp
from utils.db_api import db_commands
from utils.db_api.db_commands import get_user, get_item_filter
from utils.values import values_title, menu_values
from utils.values import others


# ----------------------------------------------- ADDING BASKET --------------------------------------------
@dp.callback_query_handler(buy_callback.filter(), state="*")
async def after_add_to_card(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # await call.answer(cache_time=60)
    user = await get_user(user_id=call.from_user.id,
                          full_name=call.from_user.full_name,
                          username=call.from_user.username)
    user_lang = user.language

    action = callback_data.get("action")
    item_id = callback_data.get("item_id")

    attr = others.get_attribute_by_language(language=user_lang)
    item = await db_commands.get_item_filter(first=True, id=item_id)
    if not item:
        await call.answer(text=values_title.NOT_FOUND_ITEM[user_lang])
        await call.message.delete()
        return

    # basketItem, create = BasketItem.objects.get_or_create(product=item, user=user)
    item_name = getattr(item, attr)
    item_id_adding = item.id

    message = call.message
    if action == others.ACTION_QUANTITY or action == others.ACTION_OTHERS:
        basketItem = BasketItem.objects.filter(product=item, user=user).first()
        quantity = 0
        if basketItem:
            quantity = basketItem.quantity
        sample_quantity = 0
        markup = await inlines.calculator_inline(language=user_lang, item_id=item.id, sample_quantity=sample_quantity)
        text = await values_title.get_text_for_calculator(quantity=quantity, language=user_lang, item=item,
                                                          sample_quantity=sample_quantity)
        if call.message.caption:
            await call.message.edit_caption(caption=text, reply_markup=markup)
        elif call.message.text:
            await call.message.edit_text(text=text, reply_markup=markup)
        else:
            await call.message.delete()

        # quantity = basketItem.quantity
        # await call.answer(text=str(quantity))
        #
        # await state.update_data(item_id_adding=item_id_adding)
        # await botControl.after_item_to_basket(language=user_lang, call=call, state=state, item_name=item_name, user=user)

        return

    basketItem, create = BasketItem.objects.get_or_create(product=item, user=user)
    quantity = 0
    if action == others.ACTION_PLUS:
        basketItem.quantity = (basketItem.quantity if not create else 0) + 1
        basketItem.save()

        quantity = basketItem.quantity
    elif action == others.ACTION_MINUS or action == others.ACTION_DELETE:
        if basketItem.quantity <= 1 or action == others.ACTION_DELETE:
            basketItem.delete()
            await call.answer(text=others.CLEARED_BASKET[user_lang])

            quantity = 0

        else:
            basketItem.quantity = (basketItem.quantity if not create else 0) - 1
            basketItem.save()

            quantity = basketItem.quantity

    text = await values_title.get_text_for_item(basket_item=basketItem, language=user_lang, quantity=quantity)
    markup = await inlines.add_to_basket(language=user_lang,
                                         item_id=item_id,
                                         quantity=quantity)
    if action == others.ACTION_DELETE:
        markup = None

    if call.message.caption:
        delete_media_send_text = False
        if delete_media_send_text:
            await call.message.delete()
            await call.message.answer(text=text,
                                      reply_markup=markup)
        else:
            await call.message.edit_caption(caption=text,
                                            reply_markup=markup)
    elif call.message.text:
        await call.message.edit_text(text=text,
                                     reply_markup=markup)
    await botControl.show_orders(message=message, user=user)


# ---------------------------------------------- BUYING ITEM ----------------------
@dp.message_handler(AddToBasket(), state="*")
@dp.message_handler(state=StateDefault.buy_item)
async def buying_item(message: types.Message, state: FSMContext):
    text = message.text
    isKeyboardBot = (await state.get_state()) == StateDefault.buy_item.state
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    data = await state.get_data()
    saved_number = data.get("saved_number") if data.get("saved_number") else ''
    item_id_adding = data.get("item_id_adding")
    message_caption = data.get("message_caption")

    item = await get_item_filter(first=True, id=item_id_adding)
    structure_add_order = await state_data.get_structure_from_more_order()
    if structure_add_order.get('access'):
        if botControlOrder.not_available_to_the_add_order(item):
            await message.answer(text=values_title.not_allow_to_add_order(item_name=item.name, language=user_lang))
            await message.delete()
            if isinstance(message_caption, types.Message):
                await message_caption.delete()
            return

    if text in menu_values.CANCEL.values() or text in menu_values.HOME_BUTTON.values():
        await botControl.home_state(language=user_lang, message=message)
    elif text.isdigit() or (text in menu_values.READY.values() and isKeyboardBot and saved_number):
        text_int = 0
        if text.isdigit():
            text_int = int(text)
        goto = True
        if isKeyboardBot and len(saved_number) > 5 and not (text in menu_values.READY.values()):
            goto = False
        if (0 <= text_int <= 1000000 or (
                text in menu_values.READY.values() and isKeyboardBot and saved_number)) and goto:
            if text in menu_values.READY.values() or not (isKeyboardBot and text_int <= 9):
                if text in menu_values.READY.values():
                    text_int = int(saved_number)

                await botControl.after_enter_quantity(user=user, quantity=text_int, item_id_adding=item_id_adding,
                                                      language=user_lang,
                                                      message=message,
                                                      message_caption=message_caption,
                                                      message_edit=data.get("message_edit"))
                await state.update_data(item_id_adding=None, message_caption=None)
                if not structure_add_order.get('access'):
                    await botControl.reset_data_user()
            else:
                if not saved_number:
                    saved_number = text.strip()
                else:
                    saved_number = ''.join([saved_number, text])
                await state.update_data(saved_number=saved_number)

        else:
            await message.answer(values_title.DONT_HACK_ME[user_lang])
    else:
        await message.answer(values_title.WRITE_QUANTITY[user_lang])


# ---------------------------------------------- STATE: BASKET -----------------------------------
@dp.message_handler(state=StateDefault.basket)
async def basket_state(message: types.Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    user = await get_user(user_id=user_id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    is_empty = await botControl.is_empty_basket(user=user, message=message)
    if is_empty:
        return
    if text in menu_values.TO_ORDER.values():
        data = await state.get_data()
        await state.update_data(client_chosen=None)
        if user.choice_from_list_clients and user.clients.filter(access=True).count() > 0:
            await botControlOrder.choice_client(language=user_lang, message=message, user=user)
        else:
            await botControlOrder.phone_message(language=user_lang, message=message)
        # ---------------------------------- CHECK LOADING (нагрузка) ---------------------------------
        # await botControlOrder.check_nagruzka(message_2=message, user_2=user, func=botControlOrder.phone_message,
        #                                      language=user_lang, message=message)
        # ------------------------------------- END LOADING ----------------------------------------
        # await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)
        await delete_all_callback(data)
    elif text in menu_values.EDIT_QUANTITY.values():
        data = await state.get_data()
        await botControl.edit_quantity_product(language=user_lang, user=user, message=message, state=state)
        await delete_all_callback(data)
    elif text in menu_values.RESET_BASKET.values():
        await botControl.reset_basket(language=user_lang, user=user, message=message)
    elif text in menu_values.REVIEW.values():
        await botControl.review(language=user_lang, message=message)
    elif text in menu_values.HOME_BUTTON.values() or text in menu_values.BACK_BUTTON.values():
        data = await state.get_data()
        await botControl.home_state(language=user_lang, message=message)
        await delete_all_callback(data)
        await botControl.reset_data_user()
    else:
        markup = await kb.basket_keyboards(user_lang)
        await botControl.choose_below(language=user_lang, message=message, markup=markup)


async def delete_all_callback(data: dict):
    all_message_id = data.get("all_message_edit_quantity")
    if all_message_id:
        for message_id in all_message_id:
            await message_id.delete()


@dp.callback_query_handler(edit_item_callback.filter(), state="*")
async def edit_item_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # await call.answer(cache_time=60)
    action = callback_data.get("action")
    basket_id = callback_data.get("basket_id")
    res = await db_commands.get_basket_item(first=True, id=basket_id)
    user = await get_user(user_id=call.from_user.id,
                          full_name=call.from_user.full_name,
                          username=call.from_user.username)
    user_lang = user.language

    if not res:
        await call.message.delete()
        await botControl.is_empty_basket(user=user, message=call.message)
        return

    quantity = 0
    attr = others.get_attribute_by_language(language=user_lang)
    if action == others.ACTION_OTHERS or action == others.ACTION_QUANTITY:
        message = call.message

        item_name = getattr(res.product, attr)
        await state.update_data(item_id_adding=res.product.id, message_caption=message)
        await botControl.after_item_to_basket(language=user_lang, call=call, state=state, item_name=item_name,
                                              user=user)

        return

    # if action == others.ACTION_QUANTITY:
    #     quantity = res.quantity
    #     await call.answer(text=str(res.quantity))

    elif action == others.ACTION_PLUS:
        res.quantity = res.quantity + 1
        res.save()

        quantity = res.quantity
    elif action == others.ACTION_DELETE:
        res.delete()
        await call.answer(text=others.CLEARED_BASKET[user_lang])
        await call.message.edit_text(reply_markup=None,
                                     text=values_title.get_title_delete_from_basket(language=user.language,
                                                                                    product=getattr(res.product, attr)))
        quantity = 0

        return
    elif action == others.ACTION_MINUS:
        if res.quantity <= 1:
            await call.answer()
            return
        else:
            res.quantity = res.quantity - 1
            res.save()

            quantity = res.quantity

    text = await values_title.get_text_for_item(basket_item=res, language=user_lang, quantity=quantity)
    markup = await inlines.get_inline_kb_edit_item_basket(basket_id=basket_id,
                                                          quantity=res.quantity,
                                                          language=user_lang)
    await call.message.edit_text(text=text,
                                 reply_markup=markup)
    await botControl.show_orders(message=call.message, user=user)
