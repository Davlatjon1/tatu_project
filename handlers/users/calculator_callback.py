from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import LIST_KEYS_TO_THE_ADD_ORDER
from handlers import botControl, state_data, botControlOrder
from keyboards.inline import inlines
from keyboards.inline.callback_datas import calculator_callback
from loader import dp
from utils.db_api import db_commands
from utils.values import others, values_title, menu_values


@dp.callback_query_handler(calculator_callback.filter(), state="*")
async def calculator_main(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # await call.answer(cache_time=60)
    user = await db_commands.get_user(user_id=call.from_user.id,
                                      full_name=call.from_user.full_name,
                                      username=call.from_user.username)
    user_lang = user.language

    action = callback_data.get("action")
    numeral = callback_data.get("numeral")
    item_id = callback_data.get("item_id")
    sample_quantity = str(callback_data.get("sample_quantity"))

    attr = others.get_attribute_by_language(language=user_lang)
    item = await db_commands.get_item_filter(first=True, id=item_id)

    await state.update_data(item_id_adding=None)

    if not item:
        await call.answer(text=values_title.NOT_FOUND_ITEM[user_lang])
        await call.message.delete()
        return

    if not sample_quantity.isdigit() and not numeral.isdigit() or not sample_quantity and not numeral:
        await call.message.delete()
        return

    item_name = getattr(item, attr)
    item_id_adding = item.id

    quantity = 0

    structure_more_order = await state_data.get_structure_from_more_order()
    if structure_more_order['access']:
        item_more_order = await state_data.get_item_from_more_order(item)
        quantity = item_more_order['quantity']
        if botControlOrder.not_available_to_the_add_order(item):
            await call.message.answer(text=values_title.not_allow_to_add_order(item_name=item_name, language=user_lang))
            await call.message.delete()
            return

    basketItem = db_commands.BasketItem.objects.filter(product=item, user=user).first()
    if basketItem:
        quantity = basketItem.quantity

    if action == others.ACTION_QUANTITY or action == others.ACTION_ERASE:
        if action == others.ACTION_QUANTITY:
            if len(sample_quantity) >= 5:
                await call.answer(text=values_title.DONT_HACK_ME[user_lang], show_alert=True)
                return

            sample_quantity = int(f"{sample_quantity}{numeral}")
        elif action == others.ACTION_ERASE:
            if len(sample_quantity) == 1:
                sample_quantity = 0
            else:
                sample_quantity = int(sample_quantity[:-1])

        markup = await inlines.calculator_inline(language=user_lang, item_id=item_id, sample_quantity=sample_quantity)
        text = await values_title.get_text_for_calculator(quantity=quantity, item=item, language=user_lang,
                                                          sample_quantity=sample_quantity)
        if call.message.caption:
            await call.message.edit_caption(caption=text, reply_markup=markup)
        elif call.message.text:
            await call.message.edit_text(text=text, reply_markup=markup)
        else:
            await call.message.delete()
    elif action == others.ACTION_CANCEL or action == others.ACTION_READY:
        text = await values_title.get_text_for_item_2(quantity=quantity, item=item, language=user_lang)
        sample_quantity = int(sample_quantity)
        if action == others.ACTION_READY:
            if structure_more_order['access']:
                over_the_limit_add_order = await botControlOrder.over_the_limit_add_order(user=user, item=item,
                                                                                          quantity=sample_quantity)
                if over_the_limit_add_order:
                    await botControlOrder.prohibited_add_order(user=user, message=call.message)
                    return
                await state_data.update_item_to_more_order(item=item, quantity=sample_quantity)
                quantity = sample_quantity

            else:
                if not basketItem:
                    basketItem = db_commands.BasketItem(user=user, product=item)
                basketItem.quantity = sample_quantity
                basketItem.save()

                if sample_quantity == 0:
                    basketItem.delete()

                quantity = basketItem.quantity

            text = values_title.get_recorded_to_basket(item_name=item_name, quantity=quantity,
                                                       price=item.price,
                                                       language=user_lang,
                                                       remainder=item.reminder,
                                                       access_more_order=structure_more_order['access'])
        markup = await inlines.add_to_basket(language=user_lang, quantity=quantity, item_id=item.id)
        if call.message.caption:
            await call.message.edit_caption(caption=text, reply_markup=markup)
        elif call.message.text:
            await call.message.edit_text(text=text, reply_markup=markup)

        if action == others.ACTION_READY:
            await botControl.show_orders(call.message, user=user)
