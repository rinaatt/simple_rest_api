from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('credits', '0001_initial'),
        ('partners', '0001_initial'),
        ('common', '0002_organization'),
    ]

    operations = [
    ]
