from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.auth.models import User
from apps.questionnaires.models import Questionnaire


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Оганизация'
        verbose_name_plural = 'Организации'

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


class Claim(models.Model):
    NEW = 'N'
    SENT = 'S'
    STATUS_CHOICES = (
        (NEW, 'Новая'),
        (SENT, 'Отправленная'),
    )
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    created = models.DateTimeField('Создано', auto_now_add=True)
    owner = models.ForeignKey(User, models.CASCADE, verbose_name='Создатель', null=True)
    sent = models.DateTimeField('Отправлено', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, models.CASCADE, verbose_name='Анкета клиента')
    offer = models.ForeignKey(Offer, models.CASCADE, verbose_name='Предложение')
    status = models.CharField('Статус', max_length=1, choices=STATUS_CHOICES, default=NEW)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return


__all__ = [
    'Organization',
    'Offer',
    'Claim',
]
