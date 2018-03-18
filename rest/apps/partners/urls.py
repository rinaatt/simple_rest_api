from django.urls import include, path
from rest_framework import routers
from apps.questionnaires.views import QuestionnaireViewSet
from apps.claims.views import ClaimViewSet

router = routers.DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'claims', ClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
