import logging
from decimal import Decimal
from typing import List

from asgiref.sync import sync_to_async

from django_project.telegrambot.constants.models import Constants
from utils.values.values_django import STATUS_ON_THE_WAY
from django_project.telegrambot.usersmanage.models import Item, User, BasketItem, OrderItem, Order, Review, Category, \
    AdditionOrderItem, MainReview
from django_project.telegrambot.instruments_telegram.models import AboutUs, WelcomeMessage
from utils.values import menu_values, others
from datetime import datetime

from utils.values.others import get_attribute_by_language


async def get_user(user_id, full_name, username):
    user = await select_user(user_id=int(user_id), username=username)
    if not user:
        user = User(user_id=int(user_id), name=full_name, username=username, access=Constants.get_access_bot())
        user.save()

    return user


@sync_to_async
def add_user(user_id, full_name, username):
    return User(user_id=int(user_id), name=full_name, username=username, access=Constants.get_access_bot()).save()


def get_available_users(**kwargs):
    users = User.objects.filter(**kwargs, access=True).all()
    return users


@sync_to_async
def select_all_users():
    users = User.objects.all()
    return users


@sync_to_async
def select_user(user_id: int, username: str = None):
    user = User.objects.filter(user_id=user_id).first()
    # if username:
    #     user.username = username
    #     user.save()
    return user


@sync_to_async
def count_users():
    total = User.objects.all().count()
    return total


@sync_to_async
def change_language(user_id: int, language: str, user: User = None):
    if type(language) != str or language not in menu_values.CHANGE_LANGUAGE.keys():
        raise TypeError('Error with language...')
    if user:
        user.language = language
        user.save()
    else:
        user = User.objects.filter(user_id=user_id).first()
        user.language = language
        user.save()


@sync_to_async
def get_items(show_bot: bool = True):
    items = Item.objects.filter(show_bot=show_bot, category__show_bot=True).all()
    # , reminder__gt=Decimal(0.00)
    return items


@sync_to_async
def get_categories_from_items(language: str, **filters):
    attr_name = get_attribute_by_language(language=language)
    key_attr = f'category__{attr_name}'
    categories = Item.objects.filter(**filters, category__show_bot=True).values(key_attr).distinct(key_attr)
    return categories, key_attr


@sync_to_async
def get_abouts_us(language: str):
    results = AboutUs.objects.filter(language=language).all()
    return results


@sync_to_async
def get_welcomes_messages(language: str):
    results = WelcomeMessage.objects.filter(language=language).all()
    return results


@sync_to_async
def get_subcategories_or_items_by_category(language: str, category: str, subcategory: str = None,
                                           show_bot: bool = True):
    attr = others.get_attribute_by_language(language=language)
    if subcategory:
        items = Item.objects.filter(**{f'category__{attr}': category}, **{f'subcategory__{attr}': subcategory},
                                    show_bot=show_bot, category__show_bot=True).all()
    else:
        items = Item.objects.filter(**{f'category__{attr}': category},
                                    show_bot=show_bot, category__show_bot=True).all()
    return items


@sync_to_async
def get_item_filter(first: bool = False, show_bot: bool = True, limit: int = 0, **kwargs):
    items = Item.objects.filter(**kwargs, show_bot=show_bot, category__show_bot=True)
    if first:
        items = items.first()
    elif limit:
        items = items[:limit].all()
    else:
        items = items.all()
    return items


@sync_to_async
def get_basket_item(first: bool = False, count: bool = False, **kwargs):
    basket_items = BasketItem.objects.filter(**kwargs)
    if count:
        res_items = basket_items.all().count()
    elif first:
        res_items = basket_items.first()
    else:
        res_items = basket_items.all()
    return res_items


@sync_to_async
def insert_basket_item(**kwargs):
    basket_item, create = BasketItem.objects.get_or_create(**kwargs)
    return basket_item


async def get_or_create_basket(user: User, product: Item, first: bool = False):
    basket_items = await get_basket_item(first=first, user=user, product=product)
    if not basket_items:
        inserted = await insert_basket_item(user=user, product=product)
        if not first:
            basket_items = [inserted]
        else:
            basket_items = inserted

    return basket_items


@sync_to_async
def delete_all_basket_by_user(user: User):
    result = False
    try:
        BasketItem.objects.filter(user=user).all().delete()
        result = True
    except Exception as err:
        logging.error(err)
    return result


@sync_to_async
def save_order_and_delete_basket(user, basket_items, order_status: str = STATUS_ON_THE_WAY, order_additional_list=[],
                                 **kwargs):
    result_order_items = []
    result_additional_order = []
    objectOrder = None
    if basket_items:
        objectOrder = Order(buyer=user, **kwargs)
        objectOrder.order_status = order_status
        objectOrder.save()
        for basket_item in basket_items:
            objectOrderItem = OrderItem(order=objectOrder,
                                        product=basket_item.product,
                                        price=basket_item.product.price,
                                        quantity=basket_item.quantity)
            objectOrderItem.save()
            result_order_items.append(objectOrderItem)
        basket_items.delete()

        for order_add in order_additional_list:
            objectAdditionalOrder = AdditionOrderItem(order=objectOrder,
                                                      product=order_add['item'],
                                                      price=order_add['item'].price,
                                                      quantity=order_add['quantity'])
            objectAdditionalOrder.save()
            result_additional_order.append(objectAdditionalOrder)

    return objectOrder, result_order_items, result_additional_order


@sync_to_async
def delete_order_id(order_id):
    order = Order.objects.filter(id=int(order_id))
    if order:
        order.delete()


def set_status_order_id(order_id, order_status):
    order = Order.objects.filter(id=int(order_id)).first()
    if order:
        order.order_status = order_status
        order.save()
    return order


@sync_to_async
def get_users(**kwargs):
    users = User.objects.filter(**kwargs).all()
    return users


@sync_to_async
def get_order_filter(limit: int = None, sort: str = '-purchase_time', first: bool = False, **kwargs):
    orders = Order.objects.filter(**kwargs)
    if limit:
        if first:
            orders = orders.order_by(sort)[:limit].first()
        else:
            orders = orders.order_by(sort)[:limit].all()
    else:
        if first:
            orders = orders.order_by(sort).first()
        else:
            orders = orders.order_by(sort).all()
    return orders


@sync_to_async
def get_order_item_filter(**kwargs):
    orders = OrderItem.objects.filter(**kwargs).all()
    return orders


@sync_to_async
def get_more_order_item_filter(**kwargs):
    orders = AdditionOrderItem.objects.filter(**kwargs).all()
    return orders


@sync_to_async
def save_review(**kwargs):
    review = Review(**kwargs).save()
    return review


@sync_to_async
def get_clients_uuid_1c_inside_users(**kwargs):
    key_attr = 'client__uuid_1c'
    categories = User.objects.filter(client__uuid_1c__isnull=False, **kwargs).values(key_attr).distinct(key_attr)
    return categories, key_attr


@sync_to_async
def get_reviews_main(language: str, **kwargs):
    key_attr = get_attribute_by_language(language=language)
    main_reviews = MainReview.objects.filter(**kwargs).all()
    return main_reviews, key_attr
