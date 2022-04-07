import asyncio
import time

from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from simple_history.admin import SimpleHistoryAdmin

from handlers.botControlOrder import api_to_1c_orders_sync
from .models import (
    User,
    Item,
    Subcategory,
    Category,
    Order,
    OrderItem,
    BasketItem,
    AdditionOrderItem, MainReview, ClientUser,
)
from ..constants.models import Constants


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


class ClientUserInline(admin.TabularInline):
    model = ClientUser
    extra = 0


# class UserAdmin(admin.ModelAdmin):
class UserHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "user_id", "access", "access_act_sverki", "name", "client", "choice_from_list_clients",
        "access_group_of_counterparties", "username",
        "language", "created_at", "updated_at")
    list_filter = ['created_at', 'updated_at']
    list_display_links = ("user_id", "name")
    search_fields = ('name', 'client__name', 'username',)
    list_editable = ("access", "access_act_sverki", "client", "access_group_of_counterparties")
    inlines = [ClientUserInline, BasketItemInline]
    autocomplete_fields = ['client']


def copy_data(self, request, queryset):
    for obj in queryset:
        obj.id = None
        obj.save()


copy_data.short_description = "Скопировать"
copy_data.allowed_permissions = ('change',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id", "uuid_1c", "name", "price", "reminder", "show_bot", "subcategory", "category", "created_at", "updated_at")
    list_display_links = ('id', 'name')
    list_editable = ("show_bot",)
    search_fields = ('id', 'name', 'uuid_1c')
    actions = [copy_data]


@admin.register(MainReview)
class MainReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "show_bot", "created_at", "updated_at")
    list_display_links = ('id', 'name')
    list_editable = ("show_bot",)
    search_fields = ('id', 'name', 'uuid_1c')
    # actions = [copy_data]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "uuid_1c", 'show_bot')
    search_fields = ('id', 'name', 'uuid_1c')
    list_display_links = ('id', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ('id', 'name')


def on_update_api(self, request, queryset):
    row_update = queryset.update(update_api=True)
    if row_update == '1':
        message_bit = '1 запись была обновлена'
    else:
        message_bit = f'{row_update} записей были обновлены'
    self.message_user(request, message_bit)


on_update_api.short_description = "Включить 'update_api'"
on_update_api.allowed_permissions = ('change',)


# --------------------------------------------------

def send_using_api(self, request, queryset):
    api_to_1c_orders_sync(queryset)
    row_update = str(len(queryset))
    if row_update == '1':
        message_bit = '1 запись была обновлена'
    else:
        message_bit = f'{row_update} записей были обновлены'
    self.message_user(request, message_bit)


send_using_api.short_description = "Отправлять данные (API)"
send_using_api.allowed_permissions = ('change',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class AdditionOrderItemInline(admin.TabularInline):
    model = AdditionOrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_id', 'buyer', 'client', 'successful', 'order_status', 'note', 'purchase_time',
                    'phone_number', 'receiver', 'address', 'comment', 'type_of_payment',
                    'updated_at')
    list_filter = ['order_status', 'successful', 'purchase_time', 'created_at']
    list_display_links = ('id', 'buyer', 'order_status')
    search_fields = ('id', 'buyer__name')
    inlines = [OrderItemInline, AdditionOrderItemInline]
    actions = [on_update_api, send_using_api]


admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserHistoryAdmin)

admin.site.unregister(Group)

# admin.site.site_header = 'Admin'
