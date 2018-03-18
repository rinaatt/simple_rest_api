from django.apps import AppConfig

APP_LABEL = 'partners'


class QuestionnaireConfig(AppConfig):
    name = 'apps.partners'
    label = APP_LABEL
    verbose_name = 'Партнёры и клиенты'
