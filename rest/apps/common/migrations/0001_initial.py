from django.contrib.postgres.operations import CryptoExtension
from django.db import migrations, connections
from django.conf import settings
import environ

env = environ.Env()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        CryptoExtension(),
    ]

    def __init__(self, name, app_label):
        default_su = settings.DATABASES['default'].copy()
        default_su['USER'] = env('DATABASE_SU_USERNAME')
        default_su['PASSWORD'] = env('DATABASE_SU_PASSWORD')
        settings.DATABASES['default_su'] = default_su
        super().__init__(name, app_label)

    def __del__(self):
        del settings.DATABASES['default_su']

    def apply(self, project_state, schema_editor, collect_sql=False):
        new_schema_editor = schema_editor.connection.schema_editor()
        new_schema_editor.connection = connections['default_su']
        result = super().apply(project_state, new_schema_editor, False)
        new_schema_editor.connection.close()
        del new_schema_editor
        return result

    def unapply(self, project_state, schema_editor, collect_sql=False):
        new_schema_editor = schema_editor.connection.schema_editor()
        new_schema_editor.connection = connections['default_su']
        result = super().unapply(project_state, new_schema_editor, False)
        new_schema_editor.connection.close()
        del new_schema_editor
        return result
