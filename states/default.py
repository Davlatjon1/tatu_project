from aiogram.dispatcher.filters.state import StatesGroup, State


class StateDefault(StatesGroup):
    main = State()
    category = State()
    subcategory = State()
    item = State()
    basket = State()
    buy_item = State()  # dont understand, should be fixed
    review = State()
    review_text = State()
    act_sverki = State()


class StateOrder(StatesGroup):
    choice_client = State()
    phone = State()
    location_comment = State()
    comment = State()
    type_of_payment = State()
    is_ready_to_order = State()
    additional_order = State()
    finish_order = State()

