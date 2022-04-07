from uuid import uuid4
from django.db import models
from simple_history.models import HistoricalRecords

from data.config import LANGUAGE_RU, LANGUAGE_EN, LANGUAGE_UZ
from utils.values.values_django import ORDER_STATUSES, STATUS_ACCEPTED, STATUS_NEW, STATUS_AWAITING_SHIPMENT, \
    STATUS_ON_THE_WAY, \
    STATUS_REJECTED, \
    CASH, TERMINAL, TYPES_OF_PAYMENT

# Create your models here.
from django_project.telegrambot.contractors.models import Client

LANGUAGE_CHOICE = (
    (LANGUAGE_RU, "Русский"),
    (LANGUAGE_UZ, "Ўзбек"),
    (LANGUAGE_EN, "English"),
)

ORDER_STATUSES = (
    (STATUS_NEW, ORDER_STATUSES[STATUS_NEW].get(LANGUAGE_RU)),
    (STATUS_REJECTED, ORDER_STATUSES[STATUS_REJECTED].get(LANGUAGE_RU)),
    (STATUS_AWAITING_SHIPMENT, ORDER_STATUSES[STATUS_AWAITING_SHIPMENT].get(LANGUAGE_RU)),
    (STATUS_ON_THE_WAY, ORDER_STATUSES[STATUS_ON_THE_WAY].get(LANGUAGE_RU)),
    (STATUS_ACCEPTED, ORDER_STATUSES[STATUS_ACCEPTED].get(LANGUAGE_RU)),
)

TYPES_OF_PAYMENTS = (
    (CASH, TYPES_OF_PAYMENT[CASH].get(LANGUAGE_RU)),
    (TERMINAL, TYPES_OF_PAYMENT[TERMINAL].get(LANGUAGE_RU)),
)


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время редактирования")


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID Пользователя Телеграм", editable=False)
    name = models.CharField(max_length=100, verbose_name="Имя пользователя", null=True)
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='client')
    username = models.CharField(max_length=100, verbose_name="Username Телеграм", null=True, blank=True)
    language = models.CharField(max_length=2, default=LANGUAGE_RU, verbose_name="Язык", choices=LANGUAGE_CHOICE)
    access = models.BooleanField(verbose_name="Доступ", default=False)
    access_act_sverki = models.BooleanField(verbose_name="Доступ к акт сверки", default=False)
    access_group_of_counterparties = models.BooleanField(verbose_name='Группа контрагентов', default=False)
    history = HistoricalRecords()
    choice_from_list_clients = models.BooleanField(default=False, verbose_name='Доступ к выбору клиента')

    def __str__(self):
        return f"{self.user_id} - {self.name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class ClientUser(TimeBasedModel):
    class Meta:
        verbose_name = 'Список контрагентов'
        verbose_name_plural = 'Список контрагентов'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='clients')
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE)
    access = models.BooleanField(verbose_name='Доступ', default=False)

    def __str__(self):
        return str(self.client)


class Category(TimeBasedModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=f"Название Категории ({LANGUAGE_RU})", max_length=100)  # ,unique=True)
    name_uz = models.CharField(verbose_name=f"Название Категории ({LANGUAGE_UZ})", max_length=100)  # ,unique=True)
    name_en = models.CharField(verbose_name=f"Название Категории ({LANGUAGE_EN})", max_length=100)  # ,unique=True)
    uuid_1c = models.CharField(unique=True, verbose_name="UUID (1C)", null=True, blank=True, max_length=255,
                               editable=False)
    show_bot = models.BooleanField(verbose_name="Показывать в боте", default=True)

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Subcategory(TimeBasedModel):
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=f"Название Подкатегории ({LANGUAGE_RU})", max_length=100)  # ,unique=True
    name_uz = models.CharField(verbose_name=f"Название Подкатегории ({LANGUAGE_UZ})", max_length=100)  # ,unique=True
    name_en = models.CharField(verbose_name=f"Название Подкатегории ({LANGUAGE_EN})", max_length=100)  # ,unique=True

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Item(TimeBasedModel):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    id = models.AutoField(primary_key=True)
    uuid_1c = models.CharField(unique=True, verbose_name="UUID (1C)", null=True, blank=True, max_length=255,
                               editable=False)
    name = models.CharField(verbose_name=f"Название Продукта ({LANGUAGE_RU})", max_length=200)
    name_uz = models.CharField(verbose_name=f"Название Продукта ({LANGUAGE_UZ})", max_length=200)
    name_en = models.CharField(verbose_name=f"Название Продукта ({LANGUAGE_EN})", max_length=200)
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2, default=0)
    measure = models.CharField(verbose_name="Ед. измерения", max_length=30, null=True, blank=True, default='шт')
    price_for = models.DecimalField(verbose_name="Цена за", null=True, blank=True, decimal_places=2, max_digits=10,
                                    default=1)
    reminder = models.DecimalField(verbose_name="Остаток", max_digits=10, decimal_places=2, blank=True, null=True,
                                   default=0)

    description = models.TextField(verbose_name="Описание (ru)", null=True, blank=True)
    description_uz = models.TextField(verbose_name="Описание (uz)", null=True, blank=True)
    description_en = models.TextField(verbose_name="Описание (en)", null=True, blank=True)

    category = models.ForeignKey(Category, verbose_name="Идентификатор Категории", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, verbose_name="Идентификатор Подкатегории", on_delete=models.CASCADE,
                                    null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Выберите картинку")
    image_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID картинки")
    video_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID видео")
    show_bot = models.BooleanField(verbose_name="Показывать в боте", default=True)
    load = models.BooleanField(verbose_name="Нагрузка", default=False)
    running = models.BooleanField(verbose_name="Ходовой", default=False)

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Order(TimeBasedModel):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(editable=False, default=uuid4)
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.SET(0))
    purchase_time = models.DateTimeField(verbose_name="Время покупки", auto_now_add=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=70, null=True, blank=True)
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name='Клиент 1С', on_delete=models.SET_NULL)
    # email = models.CharField(verbose_name="Email", max_length=100, null=True, blank=True)
    order_status = models.CharField(verbose_name="Статус заказа", max_length=50, choices=ORDER_STATUSES)
    note = models.CharField(verbose_name="Примечание", max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=255, null=True, blank=True)
    longitude = models.CharField(verbose_name="Долгота (longitude)", null=True, blank=True, max_length=255)
    latitude = models.CharField(verbose_name="Широта (latitude)", null=True, blank=True, max_length=255)
    comment = models.CharField(verbose_name="Комментарий", max_length=255, null=True, blank=True)
    type_of_payment = models.CharField(verbose_name="Способ оплаты", max_length=50, null=True, blank=True,
                                       choices=TYPES_OF_PAYMENTS)
    receiver = models.CharField(verbose_name="Имя получателя", max_length=100, null=True, blank=True)
    successful = models.BooleanField(verbose_name="Оплачено", default=False)
    update_api = models.BooleanField(verbose_name="Обновить в API", editable=True, default=False)

    def __str__(self):
        return f"Заказ №{self.id}"

    def save(self, *args, **kwargs):
        self.update_api = True
        super().save(*args, **kwargs)

    def save_updated_from_api(self, *args, **kwargs):
        self.update_api = False
        super().save(*args, **kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(TimeBasedModel):
    class Meta:
        verbose_name = ""
        verbose_name_plural = "Список продуктов"

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.product.price * self.quantity


class AdditionOrderItem(TimeBasedModel):
    class Meta:
        verbose_name = "Список продуктов (доп.)"
        verbose_name_plural = "Список продуктов (доп.)"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='add_items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.product.price * self.quantity


class BasketItem(TimeBasedModel):
    class Meta:
        verbose_name = "Список продуктов (корзина)"
        verbose_name_plural = "Список продуктов (корзина)"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, related_name='basket_items', on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.product.price * self.quantity


class Review(TimeBasedModel):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    category = models.TextField(verbose_name="Категория отзыва", null=True, blank=True)


class MainReview(TimeBasedModel):
    class Meta:
        verbose_name = 'Отзыв (основной)'
        verbose_name_plural = 'Отзывы (основной)'

    name = models.CharField(verbose_name=f"Наименование ({LANGUAGE_RU})", max_length=200)
    name_uz = models.CharField(verbose_name=f"Наименование ({LANGUAGE_UZ})", max_length=200)
    name_en = models.CharField(verbose_name=f"Наименование ({LANGUAGE_EN})", max_length=200)
    show_bot = models.BooleanField(verbose_name="Показывать в боте", default=True)
