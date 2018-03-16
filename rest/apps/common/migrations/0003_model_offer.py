import django.contrib.postgres.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_model_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=django.contrib.postgres.functions.RandomUUID(), editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('rotation_start', models.DateTimeField(blank=True, null=True, verbose_name='Начало ротации')),
                ('rotation_finish', models.DateTimeField(blank=True, null=True, verbose_name='Окончание ротации')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('typ', models.CharField(choices=[('C', 'Потребительский'), ('M', 'Ипотечный'), ('A', 'Автокредит'), ('B', 'КМСБ')], default='C', max_length=1, verbose_name='Тип')),
                ('min_score', models.IntegerField(blank=True, default=0, verbose_name='Минимальный балл')),
                ('max_score', models.IntegerField(blank=True, null=True, verbose_name='Максимальный балл')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Organization', verbose_name='Кредитная организация'))
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
            },
        ),
    ]
