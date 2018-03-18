from django.conf import settings
from django.db import migrations
from django.db.backends.base.base import BaseDatabaseWrapper
from django.apps.registry import Apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from apps.common.constants import GROUP_CREDITS, GROUP_PARTNERS


CLAIM = ('claims', 'Claim')
QUESTS = ('questionnaires', 'Questionnaire')


def create_permissions(apps: Apps, schema_editor: BaseDatabaseWrapper):
    app_model_list = [CLAIM, QUESTS]
    for app_name, model_name in app_model_list:
        ModelKlass = apps.get_model(app_name, model_name)
        content_type = ContentType.objects.get_for_model(ModelKlass)
        Permission.objects.create(codename='read_%s' % model_name.lower(),
                                  name='Can read %s' % model_name.lower(),
                                  content_type=content_type)


def remove_permissions(apps: Apps, schema_editor: BaseDatabaseWrapper):
    app_model_list = [CLAIM, QUESTS]
    for app_name, model_name in app_model_list:
        ModelKlass = apps.get_model(app_name, model_name)
        content_type = ContentType.objects.get_for_model(ModelKlass)
        try:
            Permission.objects\
                .get(codename='read_%s' % model_name.lower(),
                     content_type=content_type)\
                .delete()
        except Permission.DoesNotExist:
            pass


def add_groups(apps: Apps, schema_editor: BaseDatabaseWrapper):
    Claim = apps.get_model(*CLAIM)
    Questionnaire = apps.get_model(*QUESTS)
    c_content_type = ContentType.objects.get_for_model(Claim)
    q_content_type = ContentType.objects.get_for_model(Questionnaire)
    perm_read_app = Permission.objects.get(codename='read_claim',
                                           content_type=c_content_type)
    perm_add_app = Permission.objects.get(codename='add_claim',
                                          content_type=c_content_type)
    perm_read_ws = Permission.objects.get(codename='read_questionnaire',
                                          content_type=q_content_type)
    perm_add_ws = Permission.objects.get(codename='add_questionnaire',
                                         content_type=q_content_type)
    perm_change_ws = Permission.objects.get(codename='change_questionnaire',
                                            content_type=q_content_type)
    g_credits = Group.objects.create(name=GROUP_CREDITS)
    g_credits.permissions.add(perm_read_app)
    g_credits.save()
    g_partners = Group.objects.create(name=GROUP_PARTNERS)
    g_partners.permissions.add(perm_read_ws)
    g_partners.permissions.add(perm_add_ws)
    g_partners.permissions.add(perm_add_app)
    g_partners.permissions.add(perm_change_ws)
    g_partners.save()


def del_groups(apps: Apps, schema_editor: BaseDatabaseWrapper):
    for g_name in [GROUP_CREDITS, GROUP_PARTNERS]:
        try:
            Group.objects.get(name=g_name).delete()
        except Group.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('claims', '0001_initial'),
        ('questionnaires', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=remove_permissions),
        migrations.RunPython(add_groups, reverse_code=del_groups),
    ]
