from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.auth.models import User
from apps.questionnaires.models import Questionnaire
from apps.credits.models import Offer

__all__ = (
    'Claim',
)


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
        verbose_name = 'Заявка в кредитную организацию'
        verbose_name_plural = 'Заявки в кредитные организации'

    def __str__(self):
        return
