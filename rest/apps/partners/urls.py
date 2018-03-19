from django.urls import include, path
from rest_framework import routers
from .views import QuestionnaireViewSet, ClaimViewSet


partners_router = routers.DefaultRouter()
partners_router.register(r'questionnaires', QuestionnaireViewSet,
                         base_name='partner-questionnaire')
partners_router.register(r'claims', ClaimViewSet, base_name='partner-claim')

urlpatterns = [
    path('', include(partners_router.urls)),
]
