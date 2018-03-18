from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.auth.models import User


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Кредитная организация'
        verbose_name_plural = 'Кредитные организации'

    def __str__(self):
        return self.name


class Offer(models.Model):
    CONSUMER = 'C'
    MORTGAGE = 'M'
    AUTO = 'A'
    CSMB = 'B'
    TYPE_CHOICES = (
        (CONSUMER, 'Потребительский'),
        (MORTGAGE, 'Ипотечный'),
        (AUTO, 'Автокредит'),
        (CSMB, 'КМСБ'),
    )
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)
    rotation_start = models.DateTimeField('Начало ротации', null=True, blank=True)
    rotation_finish = models.DateTimeField('Окончание ротации', null=True, blank=True)
    name = models.CharField('Название', max_length=200)
    typ = models.CharField('Тип', max_length=1, choices=TYPE_CHOICES, default=CONSUMER)
    min_score = models.IntegerField('Минимальный балл', default=0, blank=True)
    max_score = models.IntegerField('Максимальный балл', null=True, blank=True)
    organization = models.ForeignKey(Organization, models.CASCADE,
                                     verbose_name='Кредитная организация')

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return self.name

    @property
    def type(self):
        return self.get_typ_display()


__all__ = [
    'Organization',
    'Offer',
]
