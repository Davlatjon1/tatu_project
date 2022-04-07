from django.db import models
# Create your models here.


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время редактирования")


class Branch(TimeBasedModel):
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    id = models.AutoField(primary_key=True)
    uuid_1c = models.CharField(verbose_name="UUID (1C)", null=True, blank=True, max_length=255, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=255)

    def __str__(self):
        return f"№{self.id} - {self.name}"


class Client(TimeBasedModel):
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    id = models.AutoField(primary_key=True)
    uuid_1c = models.CharField(verbose_name="UUID (1C)", null=True, blank=True, max_length=255, editable=False)
    name = models.CharField(verbose_name="Наименование", max_length=200)
    deletion_mark = models.BooleanField(verbose_name="Пометка удаления", default=False)
    branch = models.ForeignKey(Branch, verbose_name="Идентификатор Филиал", on_delete=models.CASCADE, null=True, blank=True)
    territory = models.CharField(verbose_name="Территория", max_length=200, null=True, blank=True)
    days_of_the_week = models.CharField(verbose_name="Дни недели", max_length=200, null=True, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=200, null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"№{self.id} - {self.name}"
