import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
import re
from requests.auth import HTTPBasicAuth
from utils.values.values_django import STATUS_AWAITING_SHIPMENT, STATUS_ON_THE_WAY
from django_project.telegrambot.contractors.models import Client
from handlers import botControl, botControlOrder
from handlers.botControlOrder import api_to_1c_orders
from keyboards.inline.inlines import refresh_order_inline
from keyboards.inline.callback_datas import finish_order_callback, my_order_callback
from loader import dp
from states.default import StateOrder
from utils import instruments
from utils.db_api import db_commands
from utils.db_api.db_commands import get_user
from utils.values import menu_values, values_title, values_django
from utils.values.others import get_attribute_by_language


@dp.message_handler(state=StateOrder.choice_client)
async def choice_client_state(message: types.Message, state: FSMContext):
    text = message.text
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    if text in menu_values.BACK_BUTTON.values():
        await botControl.after_basket(message=message, language=user_lang, user=user)
    else:
        client = Client.objects.filter(name=text).first()
        if client:
            await state.update_data(client_chosen=client)
            await botControlOrder.phone_message(language=user_lang, message=message)
        else:
            await botControl.not_found_client(language=user_lang, message=message)


@dp.message_handler(state=StateOrder.phone, content_types=['text', 'contact'])
async def phone_message(message: types.Message, state: FSMContext):
    await botControl.reset_data_user()

    result_phone_number = None
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    if message.contact:
        result_phone_number = message.contact.phone_number
    elif message.text:
        text = message.text
        if text in menu_values.CANCEL.values():
            await botControl.home_state(message=message, language=user_lang)
            return
        elif text in menu_values.BACK_BUTTON.values():
            if user.choice_from_list_clients and user.clients.filter(access=True).count() > 0:
                await botControlOrder.choice_client(language=user_lang, message=message, user=user)
            else:
                await botControl.after_basket(message=message, language=user_lang, user=user)
            return
        else:
            phones_number = text.replace(' ', '').split(',')
            for phone_number in phones_number:
                if not (re.match(r'[+]{1}998[0-9]{9}', phone_number) and len(phone_number) == 13):
                    await botControlOrder.phone_message(language=user_lang, message=message)
                    return
            result_phone_number = ', '.join(phones_number)
    else:
        await botControlOrder.phone_message(language=user_lang, message=message)

    if result_phone_number:
        await botControlOrder.comment_message(language=user_lang, message=message)
        # await botControlOrder.location_message(language=user_lang, message=message)
        await state.update_data(phone_number=result_phone_number)


@dp.message_handler(state=StateOrder.location_comment, content_types=['location', 'text'])
async def location_message(message: types.Message, state: FSMContext):
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)

    user_lang = user.language
    if message.location:
        # await botControlOrder.type_of_payment_message(language=user_lang, message=message)
        await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)
        location = message.location
        await state.update_data(longitude=location.longitude)
        await state.update_data(latitude=location.latitude)
        result_location = await instruments.get_address(latitude=location.latitude, longitude=location.longitude)
        await state.update_data(location=result_location)

    elif message.text:
        text = message.text
        if text in menu_values.CANCEL.values():
            await botControl.home_state(message=message, language=user_lang)
        elif text in menu_values.BACK_BUTTON.values():
            await botControlOrder.phone_message(language=user_lang, message=message)
        else:
            if text not in menu_values.SKIP_BUTTON.values():
                await state.update_data(location=text)
            # await botControlOrder.type_of_payment_message(language=user_lang, message=message)
            # await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)
            await botControlOrder.comment_message(language=user_lang, message=message)
    else:
        await botControlOrder.location_message(language=user_lang, message=message)


@dp.message_handler(state=StateOrder.type_of_payment)
async def to_confirm_order(message: types.Message, state: FSMContext):
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    text = message.text
    if text in values_django.TYPES_OF_PAYMENT[values_django.CASH].values() or text in values_django.TYPES_OF_PAYMENT[
        values_django.TERMINAL].values():
        await state.update_data(type_of_payment=text)
        await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)
    elif text in menu_values.BACK_BUTTON.values():
        await botControlOrder.location_message(language=user_lang, message=message)
    else:
        await botControlOrder.type_of_payment_message(language=user_lang, message=message)


@dp.message_handler(state=StateOrder.comment)
async def to_confirm_order(message: types.Message, state: FSMContext):
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    text = message.text
    if text in menu_values.BACK_BUTTON.values():
        # await botControlOrder.location_message(language=user_lang, message=message)
        await botControlOrder.phone_message(language=user_lang, message=message)
    elif text in menu_values.SKIP_BUTTON.values():
        await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)
    else:
        await state.update_data(comment=text)
        await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)


@dp.message_handler(state=StateOrder.is_ready_to_order)
async def is_ready_to_order_message(message: types.Message, state: FSMContext):
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    text = message.text
    if text in menu_values.CANCEL.values():
        await botControl.home_state(language=user_lang, message=message)
    elif text in menu_values.TO_CONFIRM.values():
        # -------------------------------- CHECK LOAD (нагрузка) ------------------------
        # await botControlOrder.check_nagruzka(message_2=message, user_2=user, func=botControlOrder.additional_order,
        #                                      message=message, user=user)
        # ---------------------------------- END LOAD ----------------------------
        await botControlOrder.finish_order(message=message, language=user_lang, user=user)
        # await botControlOrder.additional_order(message=message, user=user)
    else:
        await botControlOrder.to_confirm_message(language=user_lang, message=message, user=user)


@dp.callback_query_handler(finish_order_callback.filter(), state="*")
async def finish_call_query(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user = await get_user(user_id=call.from_user.id,
                          full_name=call.from_user.full_name,
                          username=call.from_user.username)
    user_lang = user.language
    data = await state.get_data()
    message_in_delete = data.get("message_in_delete")
    order_id = data.get("order_id")
    if message_in_delete:
        await message_in_delete.delete()

    await call.message.edit_text(values_title.get_canceled_order(order_id, user_lang), reply_markup=None)
    order = db_commands.set_status_order_id(order_id,
                                            values_django.STATUS_REJECTED)  # await db_commands.delete_order_id(order_id=order_id)
    await api_to_1c_orders([order])


# ---------------------------------- CLICKING REFRESH MY ORDER ---------------------------------

@dp.callback_query_handler(my_order_callback.filter(), state="*")
async def my_order_call_query(call: types.CallbackQuery, callback_data: dict):
    user = await get_user(user_id=call.from_user.id,
                          full_name=call.from_user.full_name,
                          username=call.from_user.username)
    user_lang = user.language
    order_id = callback_data.get("order_id")
    order_by_id = await db_commands.get_order_filter(id=order_id, first=True)
    if order_by_id:

        markup = await refresh_order_inline(user_lang, order_by_id.id)
        if order_by_id.order_status not in (STATUS_AWAITING_SHIPMENT, STATUS_ON_THE_WAY):
            markup = None

        order_text = await values_title.title_my_order(user_lang, order_by_id)
        await botControlOrder.split_message(message=call, text=order_text, markup=markup)
        await call.message.delete()
    else:
        await call.message.delete()
