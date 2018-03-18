from django.apps import AppConfig

APP_LABEL = 'credits'


class CreditsConfig(AppConfig):
    name = 'apps.credits'
    label = APP_LABEL
    verbose_name = 'Кредитные организации'
