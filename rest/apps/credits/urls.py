from django.urls import include, path
from rest_framework import routers
from apps.credits.views import ClaimViewSet

router = routers.DefaultRouter()
router.register(r'claims', ClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
