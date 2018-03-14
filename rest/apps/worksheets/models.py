from itertools import islice
from random import choice, randint
from mimesis import Person, Datetime
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
from django.db import models
from django.contrib.postgres.functions import RandomUUID


def _generate_worksheet_data(locale='ru'):
    person = Person(locale)
    rus_spec = RussiaSpecProvider()
    datetime = Datetime(locale)
    g = choice([Gender.FEMALE, Gender.MALE])
    return {
        'surname': person.surname(gender=g),
        'first_name': person.name(gender=g),
        'patronymic': rus_spec.patronymic(gender=g),
        'birth_date': datetime.datetime(start=1960, end=1998).date(),
        'phone_num': person.telephone(),
        'pass_ser': rus_spec.passport_series(),
        'pass_num': rus_spec.passport_number(),
        'score': randint(0, 2000),
    }


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

    def __str__(self):
        return self.full_name

    @staticmethod
    def _bootstrap(count=100000, locale='ru', batch_size=100):
        Worksheet.objects.all().delete()
        worksheets_gen = (Worksheet(**_generate_worksheet_data(locale))
                          for _ in range(count))
        while True:
            batch = list(islice(worksheets_gen, batch_size))
            if not batch:
                break
            Worksheet.objects.bulk_create(batch, batch_size)
