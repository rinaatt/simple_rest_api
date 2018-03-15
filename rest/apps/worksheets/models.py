from django.db import models
from django.contrib.postgres.functions import RandomUUID


class Worksheet(models.Model):
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

    class Meta:
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиента'

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
