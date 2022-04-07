from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import MORE_ORDER_CHECK_COUNT
from handlers import botControlOrder, botControl
from handlers.state_data import update_more_order, get_structure_from_more_order
from loader import dp
from states.default import StateOrder
from utils.db_api.db_commands import get_user
from utils.values import menu_values, values_title


@dp.message_handler(state=StateOrder.additional_order)
async def additional_order(message: types.Message, state: FSMContext):
    user = await get_user(user_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    user_lang = user.language
    text = message.text

    more_order = await get_structure_from_more_order()
    if text in menu_values.CANCEL.values():
        await update_more_order(reset_list=True, access=False, check_access=False)
        await botControl.home_state(language=user_lang, message=message)
    elif text in menu_values.RESET_ADDITIONAL_ORDER.values():
        await update_more_order(reset_list=True, access=True, check_access=False)
        await message.answer(values_title.ADDITIONAL_ORDER_EMPTIED[user_lang])
        await botControl.show_orders(message=message, user=user)
    elif text in menu_values.TO_CONFIRM.values():
        if MORE_ORDER_CHECK_COUNT and len(more_order['order_list']) == 0 and user.get_total_quantity() > 20:
            await botControlOrder.fill_in_the_add_order(user=user, message=message)
        else:
            await botControlOrder.finish_order(message=message, language=user_lang, user=user)
    else:
        await botControlOrder.additional_order(message=message, user=user, reset_data=False)