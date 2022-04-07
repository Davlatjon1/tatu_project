from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.values import menu_values, others
from keyboards.inline.callback_datas import buy_callback, edit_item_callback, finish_order_callback, my_order_callback, \
    calculator_callback


async def add_to_basket(language: str, item_id: int, quantity: int = 0):
    markup = InlineKeyboardMarkup(row_width=3)
    # markup.row(InlineKeyboardButton(text=menu_values.ADD_BASKET[language],
    #                                 callback_data=buy_callback.new(item_buy=item_buy, quantity=quantity)))
    # markup.row(InlineKeyboardButton(text=menu_values.MINUS_emoji,
    #                                 callback_data=buy_callback.new(action=others.ACTION_MINUS, quantity=quantity,
    #                                                                item_id=item_id)),
    markup.row(InlineKeyboardButton(text=str(quantity),
                                    callback_data=buy_callback.new(action=others.ACTION_QUANTITY, quantity=quantity,
                                                                   item_id=item_id)))
    # InlineKeyboardButton(text=menu_values.PLUS_emoji,
    #                      callback_data=buy_callback.new(action=others.ACTION_PLUS, quantity=quantity,
    #                                                     item_id=item_id)))
    # markup.row(InlineKeyboardButton(text=menu_values.CANCEL_emoji,
    #                                 callback_data=buy_callback.new(quantity=quantity, action=others.ACTION_DELETE,
    #                                                                item_id=item_id)),
    #            InlineKeyboardButton(text=menu_values.OTHERS[language],
    #                                 callback_data=buy_callback.new(quantity=quantity, action=others.ACTION_OTHERS,
    #                                                                item_id=item_id)))

    return markup


async def get_inline_kb_edit_item_basket(basket_id: Union[str, int], quantity: Union[str, int], language: str):
    markup = InlineKeyboardMarkup()
    # markup.row(InlineKeyboardButton(text=menu_values.MINUS_emoji,
    #                                 callback_data=edit_item_callback.new(basket_id=basket_id, quantity=quantity,
    #                                                                      action=others.ACTION_MINUS)),
    markup.row(InlineKeyboardButton(text=str(quantity),
                                    callback_data=edit_item_callback.new(basket_id=basket_id, quantity=quantity,
                                                                         action=others.ACTION_QUANTITY)))
    # InlineKeyboardButton(text=menu_values.PLUS_emoji,
    #                      callback_data=edit_item_callback.new(basket_id=basket_id, quantity=quantity,
    #                                                           action=others.ACTION_PLUS)),
    # )
    # markup.row(InlineKeyboardButton(text=menu_values.CANCEL_emoji,
    #                                 callback_data=edit_item_callback.new(basket_id=basket_id, quantity=quantity,
    #                                                                      action=others.ACTION_DELETE)),
    #            InlineKeyboardButton(text=menu_values.OTHERS[language],
    #                                 callback_data=edit_item_callback.new(basket_id=basket_id, quantity=quantity,
    #                                                                      action=others.ACTION_OTHERS)))
    return markup


async def finish_order_inline(language: str, order_id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=menu_values.CANCEL[language],
                                    callback_data=finish_order_callback.new(order_id=int(order_id))))
    return markup


async def refresh_order_inline(language: str, order_id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=menu_values.UPDATE[language],
                                    callback_data=my_order_callback.new(order_id=int(order_id))))
    return markup


async def search_inline(language: str):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text=menu_values.SEARCH[language],
                                       switch_inline_query_current_chat=""))

    return markup


async def calculator_inline(language: str, item_id: int, sample_quantity: Union[int, str] = 0):
    markup = InlineKeyboardMarkup(row_width=3)
    for i in range(1, 10):
        markup.insert(
            InlineKeyboardButton(text=str(i),
                                 callback_data=calculator_callback.new(action=others.ACTION_QUANTITY,
                                                                       item_id=item_id,
                                                                       numeral=i,
                                                                       sample_quantity=sample_quantity)))
    markup.row(
        InlineKeyboardButton(text=str(0),
                             callback_data=calculator_callback.new(action=others.ACTION_QUANTITY,
                                                                   item_id=item_id,
                                                                   numeral=0,
                                                                   sample_quantity=sample_quantity)),
        InlineKeyboardButton(text='↩',
                             callback_data=calculator_callback.new(action=others.ACTION_ERASE,
                                                                   item_id=item_id,
                                                                   numeral='unknown',
                                                                   sample_quantity=sample_quantity)),
    )
    markup.row(InlineKeyboardButton(text=menu_values.CANCEL[language],
                                    callback_data=calculator_callback.new(action=others.ACTION_CANCEL,
                                                                          item_id=item_id,
                                                                          numeral='unknown',
                                                                          sample_quantity=sample_quantity)),
               InlineKeyboardButton(text=menu_values.READY[language],
                                    callback_data=calculator_callback.new(action=others.ACTION_READY,
                                                                          item_id=item_id,
                                                                          numeral='unknown',
                                                                          sample_quantity=sample_quantity)
                                    ),
               )
    return markup

