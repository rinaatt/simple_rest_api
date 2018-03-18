from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.auth.models import User
from apps.common.models import Organization as CommonOrganization

__all__ = [
    'Organization',
    'Questionnaire',
]


class OrganizationManager(CommonOrganization.objects.__class__):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(typ=CommonOrganization.PARTNER).order_by('name')


class Organization(CommonOrganization):
    objects = OrganizationManager()

    class Meta:
        proxy = True
        verbose_name = 'Оганизация'
        verbose_name_plural = 'Организации'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.typ = CommonOrganization.PARTNER
        return super().save(force_insert, force_update, using, update_fields)


class Questionnaire(models.Model):
    id = models.UUIDField(primary_key=True, default=RandomUUID(), editable=False)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)
    surname = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100)
    birth_date = models.DateField('Дата рождения')
    phone_num = models.CharField('Номер телефона', max_length=30)
    pass_ser = models.CharField('Серия паспорта', max_length=5)
    pass_num = models.CharField('Номер паспорта', max_length=6)
    score = models.IntegerField('Скоринговый балл', blank=True, null=True)
    organization = models.ForeignKey(Organization, models.CASCADE,
                                     verbose_name='Партнёр', null=True)

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    @property
    def full_name(self):
        return ' '.join((self.surname, self.first_name, self.patronymic))

    @property
    def passport(self):
        return '{} {}'.format(self.pass_ser, self.pass_num)

    @passport.setter
    def passport(self, value):
        val = str(value).replace(' ', '')
        self.pass_ser = '{} {}'.format(val[0:2], val[2:4])
        self.pass_num = val[4:]

    @passport.deleter
    def passport(self):
        self.pass_ser = None
        self.pass_num = None

    def __str__(self):
        return self.full_name
