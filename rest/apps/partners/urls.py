from django.urls import include, path
from rest_framework import routers
from .views import QuestionnaireViewSet, ClaimViewSet

router = routers.DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'claims', ClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
