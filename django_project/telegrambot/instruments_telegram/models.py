from django.db import models
from django_project.telegrambot.usersmanage.models import TimeBasedModel
from data.config import LANGUAGE_RU
# Create your models here.
from django_project.telegrambot.usersmanage.models import LANGUAGE_CHOICE


class AboutUs(TimeBasedModel):
    class Meta:
        verbose_name = "Сообщение пользователю (О нас)"
        verbose_name_plural = "Сообщение пользователю (О нас)"

    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, default=LANGUAGE_RU, unique=True, verbose_name="Язык",
                                choices=LANGUAGE_CHOICE)
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Заглавие")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Выберите картинку")
    image_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID картинки")
    video_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID видео")
    latitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Широта (latitude)")
    longitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Долгота (longitude)")

    def __str__(self):
        return f"№{self.id} - {self.language}"


class WelcomeMessage(TimeBasedModel):
    class Meta:
        verbose_name = "Сообщение пользователю (Welcome)"
        verbose_name_plural = "Сообщение пользователю (Welcome)"

    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, default=LANGUAGE_RU, unique=True, verbose_name="Язык",
                                choices=LANGUAGE_CHOICE)
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Заглавие")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Выберите картинку")
    image_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID картинки")
    video_url_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID видео")
    latitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Широта (latitude)")
    longitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Долгота (longitude)")

    def __str__(self):
        return f"№{self.id} - {self.language}"
