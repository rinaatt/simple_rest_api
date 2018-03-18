# Generated by Django 2.0.3 on 2018-03-18 15:07

from django.conf import settings
import django.contrib.postgres.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.UUIDField(default=django.contrib.postgres.functions.RandomUUID(), editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('phone_num', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('pass_ser', models.CharField(max_length=5, verbose_name='Серия паспорта')),
                ('pass_num', models.CharField(max_length=6, verbose_name='Номер паспорта')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='Скоринговый балл')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Партнёр')),
            ],
            options={
                'verbose_name': 'Анкета',
                'verbose_name_plural': 'Анкеты',
            },
        ),
    ]
