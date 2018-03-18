from django.urls import include, path
from rest_framework import routers
from apps.applications.views import ApplicationViewSet

router = routers.DefaultRouter()
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
