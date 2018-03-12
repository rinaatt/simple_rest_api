from django.apps import AppConfig

APP_LABEL = 'common'


class CommonConfig(AppConfig):
    name = 'apps.common'
    label = APP_LABEL
    verbose_name = 'Общее'
