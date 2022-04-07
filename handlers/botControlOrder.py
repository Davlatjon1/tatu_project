import requests
from aiogram import types
import asyncio
import logging
from requests.auth import HTTPBasicAuth
from typing import Union
from data import config
from data.config import MAX_ROW
from django_project.telegrambot.constants.models import Constants
from utils.values.values_django import STATUS_AWAITING_SHIPMENT, STATUS_ON_THE_WAY, TYPES_OF_PAYMENT, STATUS_NEW
from django_project.telegrambot.usersmanage.models import User, Item, Order
from handlers import botControl, state_data
from handlers.state_data import update_more_order
from keyboards.default import keyboards as kb
from keyboards.inline import inlines
from loader import dp
from states.default import StateOrder
from utils.db_api import db_commands
from utils.values import values_title
from utils.values.others import get_attribute_by_language
from django_project.telegrambot.instruments_telegram.views import order_structure


async def phone_message(language: str, message: types.Message):
    markup = kb.phone_keyboards(language)
    await message.answer(text=values_title.SEND_NUMBER[language], reply_markup=markup)
    await StateOrder.phone.set()


async def choice_client(language: str, message: types.Message, user: User):
    markup = kb.clients_keyboards(language=language,
                                  list_clients=[(row_client.client.name if row_client.client else '') for row_client in
                                                user.clients.filter(access=True).all()])
    await message.answer(text=values_title.CHOOSE_CLIENT[language], reply_markup=markup)
    await StateOrder.choice_client.set()


async def location_message(language: str, message: types.Message):
    markup = kb.location_keyboards(language)
    await message.answer(text=values_title.SEND_LOCATION[language],
                         reply_markup=markup)
    await StateOrder.location_comment.set()


async def type_of_payment_message(language: str, message: types.Message):
    markup = kb.type_of_payments_keyboards(language)
    await message.answer(text=values_title.SEND_ME_TYPE_OF_PAYMENTS[language],
                         reply_markup=markup)
    await StateOrder.type_of_payment.set()


async def to_confirm_message(language: str, message: types.Message, user: User):
    basket_items = await db_commands.get_basket_item(user=user)
    if len(basket_items) == 0:
        await botControl.send_no_baskets(message=message, language=language)
        return
    confirm_text = await values_title.title_confirm_order(language, basket_items)
    markup = kb.to_confirm(language)

    await split_message(message=message, text=confirm_text, markup=markup)
    await StateOrder.is_ready_to_order.set()


async def split_message(message: Union[types.Message, types.CallbackQuery], text: str, markup,
                        give_markup: bool = True):
    results = []
    if isinstance(message, types.CallbackQuery):
        message = message.message
    text = text.strip()
    text_split = text.splitlines()
    len_text_split = len(text_split)
    index_row = 0
    while index_row + MAX_ROW < len_text_split:
        result_text = '\n'.join(text_split[index_row:index_row + MAX_ROW])
        index_row += MAX_ROW
        results_message = await message.answer(result_text)

    if not give_markup:
        dict_attr = {}
    else:
        dict_attr = {'reply_markup': markup}
    message_accepted = await message.answer('\n'.join(text_split[index_row:index_row + MAX_ROW]), **dict_attr)
    results.append(message_accepted)
    return message_accepted, results


async def comment_message(language: str, message: types.Message):
    markup = kb.back_next_keyboards(language=language)
    await message.answer(text=values_title.REVIEW_MESSAGE[language], reply_markup=markup)
    await StateOrder.comment.set()


async def finish_order(message: types.Message, language: str, user: User):
    basket_items = await db_commands.get_basket_item(user=user)
    if len(basket_items) == 0:
        await botControl.send_no_baskets(message=message, language=language)
        return
    data = await dp.current_state().get_data()
    phone_number = data.get("phone_number")
    location = data.get("location")
    comment = data.get("comment")
    type_of_payment = data.get("type_of_payment")
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    client = data.get('client_chosen')
    if not client:
        client = user.client

    type_of_payment_value = ''
    for key, item in TYPES_OF_PAYMENT.items():
        if type_of_payment in item.values():
            type_of_payment_value = key
            break
    structure_add_order = await state_data.get_structure_from_more_order()
    order_add_list = structure_add_order.get('order_list') if structure_add_order.get(
        'order_list') else []  # order additional list
    objectOrder, order_items, order_additional_list = await db_commands.save_order_and_delete_basket(user=user,
                                                                                                     basket_items=basket_items,
                                                                                                     order_status=STATUS_NEW,
                                                                                                     order_additional_list=order_add_list,
                                                                                                     phone_number=phone_number,
                                                                                                     address=location,
                                                                                                     comment=comment,
                                                                                                     type_of_payment=type_of_payment_value,
                                                                                                     latitude=latitude,
                                                                                                     longitude=longitude,
                                                                                                     client=client)
    await state_data.update_more_order(reset_list=True, access=False, check_access=False)
    order_id = objectOrder.id

    await api_to_1c_orders([objectOrder])

    order_text = await values_title.title_accepted_order(language=language, basket_items=order_items, id=order_id,
                                                         order_additional_list=order_additional_list)
    markup = await inlines.finish_order_inline(language=language, order_id=order_id)
    message_accepted, _results = await split_message(message=message, text=order_text, markup=markup)

    constant: Constants = Constants.default_constant()
    timeout_cancel_order = constant.timeout_cancel_order

    await dp.current_state().update_data(order_id=order_id)
    if timeout_cancel_order > 0:
        delete_message = await message.answer(
            values_title.opportunity_delete_order(language, constant.timeout_cancel_order))
        await dp.current_state().update_data(message_in_delete=delete_message)
    await botControl.home_state(language, message, False)

    if timeout_cancel_order > 0:
        await asyncio.sleep(timeout_cancel_order)
        try:
            await delete_message.delete()
        except Exception as er:
            pass

    if message_accepted:
        try:
            await message_accepted.edit_reply_markup(reply_markup=None)
        except Exception as er:
            pass
    await botControl.reset_data_user()


async def my_orders(user: User, message: types.Message):
    orders_by_user = await db_commands.get_order_filter(limit=3, sort='-purchase_time', buyer=user)
    user_lang = user.language
    if len(orders_by_user) == 0 or not orders_by_user:
        await message.answer(values_title.EMPTY_ORDER[user_lang], reply_markup=await kb.main_keyboards(user_lang))
        return
    for order in orders_by_user:
        order_text = await values_title.title_my_order(user_lang, order)
        markup = await inlines.refresh_order_inline(user_lang, order.id)
        if order.order_status not in (STATUS_AWAITING_SHIPMENT, STATUS_ON_THE_WAY):
            markup = None
        await split_message(message=message, text=order_text, markup=markup)


async def api_to_1c_orders(objectsOrder):
    constant: Constants = Constants.default_constant()
    if not (constant.setting_api is not None and constant.setting_api.url_to_update_order):
        return
    try:
        data = {}
        order_structure(objectsOrder, data, uncheck_api=False)
        response = ready_request(params=data, url=constant.setting_api.url_to_update_order)
        if response.status_code == 200:
            params = response.json()
            saved_orders_uuid = [line['uuid'] for line in params['saved_orders']]
            _orders = Order.objects.filter(unique_id__in=saved_orders_uuid).all()
            for _order in _orders:
                _order.save_updated_from_api()
        else:
            await botControl.send_to_group(response.text)
    except Exception as err:
        await botControl.send_to_group(str(err))


def api_to_1c_orders_sync(objectsOrder):
    constant: Constants = Constants.default_constant()
    if not (constant.setting_api is not None and constant.setting_api.url_to_update_order):
        return
    try:
        data = {}
        order_structure(objectsOrder, data, uncheck_api=False)
        response = ready_request(params=data, url=constant.setting_api.url_to_update_order)
        if response.status_code == 200:
            params = response.json()
            saved_orders_uuid = [line['uuid'] for line in params['saved_orders']]
            _orders = Order.objects.filter(unique_id__in=saved_orders_uuid).all()
            for _order in _orders:
                _order.save_updated_from_api()
        else:
            botControl.send_to_group_sync(response.text)
    except Exception as err:
        botControl.send_to_group_sync(str(err))


async def check_nagruzka(message_2: types.Message, user_2: User, func, **kwargs_func):
    data = await dp.current_state().get_data()

    user_lang = user_2.language
    await message_2.answer(values_title.LOADING[user_lang])
    basket_items = await db_commands.get_basket_item(user=user_2)
    if len(basket_items) == 0:
        await botControl.send_no_baskets(message=message_2, language=user_lang)
        return

    _client = data.get('client_chosen')
    if not _client:
        _client = user_2.client

    params = {'results': [{'uuid': basket_item.product.uuid_1c, 'quantity': basket_item.quantity} for basket_item in
                          basket_items], 'client_uuid': str('' if _client is None else _client.uuid_1c),
              "user": {'name': str(user_2.name), 'id': int(user_2.user_id)},
              'order_price': int(
                  sum([basket_item.product.price * basket_item.quantity for basket_item in basket_items]))}
    constant: Constants = Constants.default_constant()
    try:
        response = ready_request(params=params, url='check_order/')
        response_params = response.json()
        if response.status_code != 200:
            await message_2.answer(values_title.FAILURE[user_lang])
            await botControl.home_state(language=user_lang, message=message_2, reset=True)
            await botControl.send_to_group(text=f"⚠ Status code = {response.status_code}, {response_params['message']}")
        else:
            if response_params['limit_bool'] and response_params['message_limit']:
                await message_2.answer(response_params['message_limit'])
                return

            if len(response_params['results']) == 0 and len(response_params['results_remainder']) == 0 and len(
                    response_params['results_running']) == 0 and not response_params['limit_bool']:
                # await finish_order(message=message, language=user_lang, user=user)
                await func(**kwargs_func)
            else:
                text = ''
                if len(response_params['results']) > 0:
                    for res_load in response_params['types_load']:
                        total_quantity = round(res_load['quantity'])
                        text = text + f"👇 {values_title.YOU_SHOULD_BUY[user_lang]} {res_load['product_type']}: {total_quantity if total_quantity % 2 == 0 else total_quantity + 1} {values_title.UNIT_WT_low[user_lang]}\n"
                    for result in response_params['results']:
                        item = await db_commands.get_item_filter(first=True, uuid_1c=str(result['uuid']))
                        if item:
                            text += f"<b>{getattr(item, get_attribute_by_language(user_lang))}</b> ({values_title.REMAINDER[user_lang].lower()[:3]}: {int(result['quantity'])})" + '\n'
                if len(response_params['results_remainder']) > 0:
                    text = text + f"\n\n👇 {values_title.HAS_NOT_ENOUGH[user_lang]}:\n"
                    for result in response_params['results_remainder']:
                        item = await db_commands.get_item_filter(first=True, uuid_1c=str(result['uuid']))
                        if item:
                            text += f"<b>{getattr(item, get_attribute_by_language(user_lang))}:</b> {result['no_enough']}" + '\n'
                if len(response_params['results_running']) > 0:
                    text = text + f"\n\n👇 {values_title.CHANGED_QUANTITY_RUNNING[user_lang]}:\n"
                    for result in response_params['results_running']:
                        item = await db_commands.get_item_filter(first=True, uuid_1c=str(result['uuid']))
                        if item:
                            text += f"<b>{getattr(item, get_attribute_by_language(user_lang))}:</b> {int(result['quantity'])}" + '\n'
                if text:
                    # await message_2.answer(text=text)
                    await split_message(message=message_2, text=text, give_markup=False, markup=None)
                    await botControl.search(language=user_lang, message=message_2)

                if len(response_params['results']) == 0 and not response_params['limit_bool']:
                    for res in response_params['results_remainder']:
                        vrem_item = await db_commands.get_basket_item(first=True, user=user_2,
                                                                      product__uuid_1c=str(res['uuid']))
                        if vrem_item:
                            vrem_item.quantity = vrem_item.quantity - int(res['no_enough'])
                            if vrem_item.quantity <= 0:
                                vrem_item.delete()
                            else:
                                vrem_item.save()
                    for res_run in response_params['results_running']:
                        item_run = await db_commands.get_basket_item(first=True, user=user_2,
                                                                     product__uuid_1c=str(res_run['uuid']))
                        if item_run:
                            item_run.quantity = int(res_run['quantity']) + int(res_run['quantity']) % 2
                            if item_run.quantity <= 0:
                                item_run.delete()
                            else:
                                item_run.save()
                    await func(**kwargs_func)

    except Exception as err:
        await message_2.answer(values_title.FAILURE[user_lang])
        await botControl.home_state(language=user_lang, message=message_2, reset=True)
        text_error = f'Произошла ошибка: ❌ {str(err)}'
        try:
            text_error = f'❌ {err}, reason = {response.reason}, text = {response.text}'
        except:
            pass
        await botControl.send_to_group(text=text_error)


def ready_request(params: dict, url: str):
    constant: Constants = Constants.default_constant()
    return requests.post(url=url,
                         auth=HTTPBasicAuth(constant.setting_api.login_1c.encode('UTF-8'),
                                            constant.setting_api.password_1c.encode('UTF-8')),
                         json=params)


async def additional_order(message: types.Message, user: User, reset_data=True):
    if reset_data:
        await update_more_order(reset_list=True, access=True, check_access=False)

    basket_items = await db_commands.get_basket_item(user=user)
    if len(basket_items) == 0:
        await botControl.send_no_baskets(message=message, language=user.language)
        await botControl.home_state(language=user.language, message=message, reset=True)
        return

    markup = kb.additional_order(language=user.language)
    await message.answer(text=values_title.ADD_MORE_ORDER[user.language], reply_markup=markup)
    await rules_adding_add_order(user=user, message=message)
    await botControl.search(language=user.language, message=message)
    await StateOrder.additional_order.set()

    # await finish_order(message=message, language=user.language, user=user)


async def fill_in_the_add_order(message: types.Message, user: User):
    await message.answer(text=values_title.FILL_IN_THE_ADD_ORDER[user.language])


def not_available_to_the_add_order(item):
    return any(getattr(item, key) for key in config.LIST_KEYS_TO_THE_ADD_ORDER)


async def over_the_limit_add_order(user: User, item: Item, quantity) -> bool:
    total_add_order = await state_data.get_total_quantity_additional_order()
    item_add_order = await state_data.get_item_from_more_order(item=item)
    total_order_quantity = user.get_total_quantity()
    return (total_add_order + quantity - item_add_order[
        'quantity']) / total_order_quantity * 100 > config.MAX_PER_ADDITIONAL_ORDER


async def prohibited_add_order(user: User, message: types.Message):
    await message.answer(values_title.RULE_LIMIT_ADD_ORDER[user.language])


async def rules_adding_add_order(user: User, message: types.Message):
    await message.answer(values_title.RULES_ADDING_TO_ADD_ORDER[user.language])
