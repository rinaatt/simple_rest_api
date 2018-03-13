from django.db import models
from apps.worksheets.models import Worksheet
from apps.common.models import Offer

__all__ = (
    'Application',
)


class Application(models.Model):
    NEW = 'N'
    SENT = 'S'
    STATUS_CHOICES = (
        (NEW, 'Новая'),
        (SENT, 'Отправленная'),
    )
    created = models.DateTimeField('Создано', auto_now_add=True)
    sent = models.DateTimeField('Отправлено', null=True, blank=True)
    worksheet = models.ForeignKey(Worksheet, verbose_name='Анкета клиента', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, verbose_name='Предложение', on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=1, choices=STATUS_CHOICES, default=NEW)

    class Meta:
        verbose_name = 'Заявка в кредитную организацию'
        verbose_name_plural = 'Заявки в кредитную организации'

    def __str__(self):
        return
