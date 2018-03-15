# Generated by Django 2.0.2 on 2018-03-15 05:42

from django.db import migrations
from django.db.backends.base.base import BaseDatabaseWrapper
from django.apps.registry import Apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group

CREDITS_G_NAME = 'Кредитные организации'
PARTNERS_G_NAME = 'Партнёры'


def create_permissions(apps: Apps, schema_editor: BaseDatabaseWrapper):
    app_model_list = [
        ('applications', 'Application'),
        ('worksheets', 'Worksheet')
    ]
    for app_name, model_name in app_model_list:
        ModelKlass = apps.get_model(app_name, model_name)
        content_type = ContentType.objects.get_for_model(ModelKlass)
        Permission.objects.create(codename='read_%s' % model_name.lower(),
                                  name='Can read %s' % model_name.lower(),
                                  content_type=content_type)


def remove_permissions(apps: Apps, schema_editor: BaseDatabaseWrapper):
    app_model_list = [
        ('applications', 'Application'),
        ('worksheets', 'Worksheet')
    ]
    for app_name, model_name in app_model_list:
        ModelKlass = apps.get_model(app_name, model_name)
        content_type = ContentType.objects.get_for_model(ModelKlass)
        Permission.objects\
            .get(codename='read_%s' % model_name.lower(),
                 content_type=content_type)\
            .delete()


def add_groups(apps: Apps, schema_editor: BaseDatabaseWrapper):
    Application = apps.get_model('applications', 'Application')
    Worksheet = apps.get_model('worksheets', 'Worksheet')
    app_content_type = ContentType.objects.get_for_model(Application)
    ws_content_type = ContentType.objects.get_for_model(Worksheet)
    perm_read_app = Permission.objects.get(codename='read_application',
                                           content_type=app_content_type)
    perm_add_app = Permission.objects.get(codename='add_application',
                                          content_type=app_content_type)
    perm_read_ws = Permission.objects.get(codename='read_worksheet',
                                          content_type=ws_content_type)
    perm_add_ws = Permission.objects.get(codename='add_worksheet',
                                         content_type=ws_content_type)
    perm_change_ws = Permission.objects.get(codename='change_worksheet',
                                            content_type=ws_content_type)
    g_credits = Group.objects.create(name=CREDITS_G_NAME)
    g_credits.permissions.add(perm_read_app)
    g_credits.save()
    g_partners = Group.objects.create(name=PARTNERS_G_NAME)
    g_partners.permissions.add(perm_read_ws)
    g_partners.permissions.add(perm_add_ws)
    g_partners.permissions.add(perm_add_app)
    g_partners.permissions.add(perm_change_ws)
    g_partners.save()


def del_groups(apps: Apps, schema_editor: BaseDatabaseWrapper):
    Group.objects.get(name=CREDITS_G_NAME).delete()
    Group.objects.get(name=PARTNERS_G_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20180314_1238'),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=remove_permissions),
        migrations.RunPython(add_groups, reverse_code=del_groups),
    ]
