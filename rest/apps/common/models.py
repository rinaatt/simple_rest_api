from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)

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
        (CONSUMER, 'потреб'),
        (MORTGAGE, 'ипотека'),
        (AUTO, 'автокредит'),
        (CSMB, 'КМСБ'),
    )
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)
    rotation_start = models.DateTimeField('Начало ротации', null=True, blank=True)
    rotation_finish = models.DateTimeField('Окончание ротации', null=True, blank=True)
    name = models.CharField('Название', max_length=200)
    typ = models.CharField('Тип', max_length=1, choices=TYPE_CHOICES, default=CONSUMER)
    min_score = models.IntegerField('Минимальный балл', default=0, blank=True)
    max_score = models.IntegerField('Максимальный балл', null=True, blank=True)
    organization = models.ForeignKey(Organization, verbose_name='Кредитная организация', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return self.name
