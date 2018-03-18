from django.apps import AppConfig

APP_LABEL = 'questionnaires'


class QuestionnaireConfig(AppConfig):
    name = 'apps.questionnaires'
    label = APP_LABEL
    verbose_name = 'Анкеты клиентов'
