from django.urls import include, path
from rest_framework import routers
from .views import ApplicationViewSet

router = routers.DefaultRouter()
router.register(r'', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
