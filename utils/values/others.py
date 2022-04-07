from typing import Union

from data.config import LANGUAGE_RU, LANGUAGE_EN, LANGUAGE_UZ
from utils.values import values_title, menu_values

THROTTLING = {
    LANGUAGE_RU: 'Потише пожалуйста 🥺',
    LANGUAGE_UZ: 'Тинчроқ илтимос 🥺',
    LANGUAGE_EN: 'Quieter please 🥺'
}

CLEARED_BASKET = {
    LANGUAGE_RU: 'Очистен ✅',
    LANGUAGE_UZ: 'Тозаланган ✅',
    LANGUAGE_EN: 'Cleared ✅'
}


SUBCATEGORIES_OR_ITEMS = 'subcategories_or_items'
SUBCATEGORIES = 'subcategories'
ITEMS_CATEGORY = 'items_category'
ITEMS_FULL = 'items_full'

ACTION_PLUS = 'plus'
ACTION_MINUS = 'minus'
ACTION_QUANTITY = 'quantity'
ACTION_DELETE = 'delete'
ACTION_OTHERS = 'others'

ACTION_ERASE = 'erase'
ACTION_CANCEL = 'cancel'
ACTION_READY = 'ready'


def get_attribute_by_language(language: str, name_object: str = 'name'):
    attr = name_object
    if language == LANGUAGE_UZ:
        attr = f'{name_object}_uz'
    elif language == LANGUAGE_EN:
        attr = f'{name_object}_en'
    return attr


def get_basket_card(name_text: str, num: Union[str, int], language: str, remainder=0, quantity=0):
    if not quantity:
        quantity = 0
    total = num * quantity
    result = f"<b>{name_text}</b> ({values_title.get_remainder(language=language, num=remainder)})\n\n" \
             f"{values_title.get_amount(language=language, num=num)}\n" \
             f"{values_title.get_total(language=language, total=total)}"
    return result


def items_text(items, language):
    attr = get_attribute_by_language(language=language)
    text = ''
    for index, item in enumerate(items):
        text += f'{index+1}) {getattr(item, attr)}\n'
    return text
