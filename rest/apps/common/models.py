from itertools import islice
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Кредитная организация'
        verbose_name_plural = 'Кредитные организации'

    def __str__(self):
        return self.name

    @staticmethod
    def _bootstrap(count=500, locale='ru', batch_size=100):
        from mimesis import Business
        business = Business(locale)
        Organization.objects.all().delete()
        objs = (Organization(name=business.company()) for _ in range(count))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Organization.objects.bulk_create(batch, batch_size)


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

    @staticmethod
    def _bootstrap(count=10000, locale='ru', batch_size=100):
        from random import randint, choice
        from mimesis import Text, Datetime
        from pytz import UTC
        text = Text(locale)
        datetime = Datetime(locale)
        typ_choice = [Offer.CONSUMER, Offer.MORTGAGE, Offer.AUTO, Offer.CSMB]

        def rand_dt():
            _dt = datetime.datetime(start=2016, end=2018)
            return _dt.replace(tzinfo=UTC)

        def rand_txt(quantity=10):
            return ' '.join(text.words(quantity=quantity))

        Offer.objects.all().delete()
        if not Organization.objects.exists():
            Organization._bootstrap()
        organizations_id = Organization.objects.values_list('pk', flat=True)
        offers_gen = (
            Offer(rotation_start=rand_dt(),
                  rotation_finish=rand_dt(),
                  name=rand_txt(),
                  typ=choice(typ_choice),
                  min_score=randint(0, 1000),
                  max_score=randint(500, 2000),
                  organization_id=choice(organizations_id))
            for _ in range(count)
        )
        while True:
            batch = list(islice(offers_gen, batch_size))
            if not batch:
                break
            Offer.objects.bulk_create(batch, batch_size)
