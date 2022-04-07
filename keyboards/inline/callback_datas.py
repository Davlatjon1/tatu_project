from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "item_id", "quantity", "action")

edit_item_callback = CallbackData("edit_item_basket", "basket_id", "quantity", "action")

finish_order_callback = CallbackData("order", "order_id")

my_order_callback = CallbackData("my_order", "order_id")

calculator_callback = CallbackData("calculator", "item_id", "numeral", "action", "sample_quantity")
