from django.apps import AppConfig

APP_LABEL = 'partners'


class PartnersConfig(AppConfig):
    name = 'apps.partners'
    label = APP_LABEL
    verbose_name = 'Партнёры и клиенты'
