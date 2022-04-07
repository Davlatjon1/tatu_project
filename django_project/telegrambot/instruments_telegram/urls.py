from django.urls import path
from django_project.telegrambot.instruments_telegram.views import items_index, clients_index, orders_index
from django_project.telegrambot.instruments_telegram.views_category import category_index
from django_project.telegrambot.instruments_telegram.views_mailing import mailing_index
from django_project.telegrambot.usersmanage.views import get_items_index

urlpatterns = [
    path('items/', items_index, name='Items'),
    path('clients/', clients_index, name="Clients"),
    path('orders/', orders_index, name="Orders"),
    path('getItems/', get_items_index, name='getItems'),
    path('mailing/', mailing_index, name='mailing'),
    path('category/', category_index, name='category')
]
