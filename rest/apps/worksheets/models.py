from django.db import models


class Worksheet(models.Model):
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)
    surname = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100)
    birth_date = models.DateField('Дата рождения')
    phone_num = models.CharField('Номер телефона', max_length=30)
    passport = models.CharField('Номер паспорта', max_length=10)
    score = models.IntegerField('Скоринговый балл', blank=True, null=True)

    class Meta:
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиента'

    @property
    def full_name(self):
        return ' '.join((self.surname, self.first_name, self.patronymic))

    def __str__(self):
        return self.full_name
