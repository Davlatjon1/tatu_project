from typing import Union

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

from data import config
from django_project.telegrambot.constants.models import Constants
from loader import dp
from utils.values import menu_values, others, values_title, values_django


async def main_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # markup.add(
    #     menu_values.PRODUCTS[language],
    #     menu_values.BASKET[language],
    #     menu_values.ABOUT_US[language],
    #     menu_values.CHANGE_LANGUAGE[language],
    #     menu_values.MY_ORDERS[language]
    # )

    constant = Constants.default_constant()
    act_sverki = constant.setting_api is not None and constant.setting_api.url_to_act_sverki

    markup.add(
        menu_values.PRODUCTS[language],
        # menu_values.PRODUCTS_WITHOUT_PICTURE[language],
        menu_values.BASKET[language],
        menu_values.ABOUT_US[language],
        menu_values.CHANGE_LANGUAGE[language],
        menu_values.REVIEW[language],
        menu_values.MY_ORDERS[language],
    )
    if act_sverki:
        markup.insert(menu_values.ACT_OF_RECONCILIATION[language])
    markup.insert(menu_values.PRICE_LIST[language])

    return markup


async def category_keyboards(language: str, categories: Union[list, set] = None):
    if not categories:
        categories = await menu_values.get_categories(language=language)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(menu_values.BASKET[language])
    markup.add(*categories)
    markup.add(menu_values.HOME_BUTTON[language])
    return markup


async def reviews_keyboards(language: str, reviews: Union[list, set] = None):
    if not reviews:
        reviews = await menu_values.get_mainReviews(language=language, show_bot=True)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(*reviews)
    markup.add(menu_values.BACK_BUTTON[language])
    return markup


async def sub_or_item_keyboards_by_category(language: str, which: str, category: str = None,
                                            subcategory: str = None, sub_or_items: Union[list, set] = None):
    if not sub_or_items:
        sub_or_items = await menu_values.get_subcategories_or_items_by_category(language=language,
                                                                                category=category,
                                                                                subcategory=subcategory)
        sub_or_items = sub_or_items.get(which)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(menu_values.BASKET[language])
    markup.add(*sub_or_items)
    markup.row(menu_values.BACK_BUTTON[language], menu_values.HOME_BUTTON[language])
    return markup


def enter_quantity(language: str):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 10):
        markup.insert(str(i))
    markup.insert(menu_values.HOME_BUTTON[language])
    markup.insert(str(0))
    markup.insert(menu_values.READY[language])
    return markup


async def basket_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(menu_values.TO_ORDER[language])
    markup.row(menu_values.RESET_BASKET[language], menu_values.EDIT_QUANTITY[language])
    markup.row(menu_values.HOME_BUTTON[language])
    return markup


def phone_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.insert(KeyboardButton(text=menu_values.MY_CONTACT[language], request_contact=True))
    markup.insert(menu_values.BACK_BUTTON[language])
    return markup


def location_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(KeyboardButton(text=menu_values.LOCATION_BUTTON[language], request_location=True))
    markup.row(menu_values.BACK_BUTTON[language],
               menu_values.SKIP_BUTTON[language])
    return markup


def back_next_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(menu_values.BACK_BUTTON[language],
               menu_values.SKIP_BUTTON[language])
    return markup


def type_of_payments_keyboards(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(values_django.TYPES_OF_PAYMENT[values_django.CASH].get(language),
               values_django.TYPES_OF_PAYMENT[values_django.TERMINAL].get(language))
    markup.insert(menu_values.BACK_BUTTON[language])
    return markup


def clients_keyboards(language: str, list_clients: list):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.insert(menu_values.BACK_BUTTON[language])
    for client in list_clients:
        if client:
            markup.insert(client)
    return markup


def to_confirm(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(menu_values.CANCEL[language])
    markup.insert(menu_values.TO_CONFIRM[language])
    return markup


async def back_keyboard(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(menu_values.BACK_BUTTON[language])
    return markup


def period(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        values_title.DAY[language],
        values_title.WEEK[language],
        menu_values.BACK_BUTTON[language],
        values_title.MONTH[language],
    )
    return markup


def additional_order(language: str):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(menu_values.RESET_ADDITIONAL_ORDER[language])
    markup.row(
        menu_values.CANCEL[language],
        menu_values.TO_CONFIRM[language],
    )
    return markup
