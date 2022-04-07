from django.db import models

from data.config import LANGUAGE_RU
from django_project.telegrambot.usersmanage.models import TimeBasedModel, User
from utils.values import values_django


class Restrict_Users_TGBOT(TimeBasedModel):
    class Meta:
        verbose_name = 'Ограничение пользователей (ТГ БОТ)'
        verbose_name_plural = 'Ограничения пользователей (ТГ БОТ)'

    name = models.CharField(verbose_name='Наименование', default='', max_length=50)
    enabled = models.BooleanField(verbose_name='Использование', default=False)
    days = models.IntegerField(verbose_name='Количество дней неиспользования заказом', default=0)

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Restrict_Users_users(TimeBasedModel):
    class Meta:
        verbose_name = 'Список исключений'
        verbose_name_plural = 'Список исключений'

    restrict_user = models.ForeignKey(Restrict_Users_TGBOT, on_delete=models.CASCADE, related_name='disabled_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disabled = models.BooleanField(verbose_name='Не актив', default=False)


class SettingsAPI(TimeBasedModel):
    class Meta:
        verbose_name = 'Настройка (API)'
        verbose_name_plural = 'Настройки (API)'

    class TypeOfActSverki(models.TextChoices):
        TEXT = values_django.TEXT, values_django.TYPES_OF_ACT_SVERKI[values_django.TEXT].get(LANGUAGE_RU)
        FILE_PDF = values_django.FILE_PDF, values_django.TYPES_OF_ACT_SVERKI[values_django.FILE_PDF].get(LANGUAGE_RU)

    name = models.CharField(verbose_name='Наименование', max_length=255)
    login_1c = models.CharField(max_length=100, default='', blank=True, verbose_name='Логин (1С)')
    password_1c = models.CharField(max_length=100, default='', blank=True,
                                   verbose_name='Пароль (1С)')
    url_to_act_sverki = models.CharField(max_length=255, default='', blank=True,
                                         verbose_name='Ссылка на акт сверки (API)')
    url_to_update_order = models.CharField(max_length=255, default='', blank=True,
                                           verbose_name='URL Обновление/создание заказ (API)')
    url_to_check_before_order = models.CharField(max_length=255, default='', blank=True,
                                                 verbose_name='URL Проверка перед заказа (API)')

    type_of_act_sverki = models.CharField(max_length=255, default=TypeOfActSverki.FILE_PDF, blank=True,
                                          verbose_name='Тип акта сверки',
                                          choices=TypeOfActSverki.choices)
    check_before_order = models.BooleanField(default=False, verbose_name='Проверить перед заказа')

    def __str__(self):
        return f"{self.name}"


class Currency(TimeBasedModel):
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    name = models.CharField(verbose_name='Наименование', max_length=255)
    name_uz = models.CharField(verbose_name='Наименование (uz)', max_length=255)
    name_en = models.CharField(verbose_name='Наименование (en)', max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Constants(TimeBasedModel):
    class Meta:
        verbose_name = 'Константа'
        verbose_name_plural = 'Константы'

    name = models.CharField(verbose_name='Наименование', max_length=255)
    restrict_users = models.ForeignKey(Restrict_Users_TGBOT, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name='Ограничение пользователей (ТГ БОТ)')
    setting_api = models.ForeignKey(SettingsAPI, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Настройка (API)')
    currency = models.ForeignKey(Currency, verbose_name='Основная валюта', on_delete=models.CASCADE, blank=True,
                                 null=True)
    timeout_cancel_order = models.IntegerField(default=0, verbose_name='Таймаут отказа заказа', blank=True)

    def channels_tg(self):
        return [res.channel_id for res in self.channels.all()]

    @staticmethod
    def default_constant():
        return Constants.objects.first()

    def __str__(self):
        return f'№{self.id} - Константа'


class Channel(TimeBasedModel):
    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    constant = models.ForeignKey(Constants, on_delete=models.CASCADE, verbose_name='Константа',
                                 related_name='channels')
    channel_id = models.CharField(default='', verbose_name='Канал (ID)', max_length=100)

    def __str__(self):
        return f'{self.id} - {self.channel_id}'
