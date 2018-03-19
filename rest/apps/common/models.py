from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.auth.models import User

__all__ = [
    'Organization',
]


class Organization(models.Model):
    CREDIT = 1
    PARTNER = 2
    TYP_CHOICES = (
        (None, 'Неизвестно'),
        (CREDIT, 'Кредитная'),
        (PARTNER, 'Партнёрская'),
    )
    CREDITS_API = '/credits/'
    PARTNERS_API = '/partners/'
    API_URL_CHOICES = (
        (CREDITS_API, 'Кредитное API'),
        (PARTNERS_API, 'Партнерское API'),
    )
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, models.CASCADE,
                                verbose_name='Пользователь',
                                related_name='organization')
    api_access = models.CharField('Доступ к API', max_length=20, null=True,
                                  blank=True, choices=API_URL_CHOICES)
    typ = models.SmallIntegerField('Тип организации', choices=TYP_CHOICES,
                                   db_index=True, editable=False)

    def __str__(self):
        return self.name
