from django.urls import include, path
from rest_framework import routers
from .views import ClaimViewSet


credits_router = routers.DefaultRouter()
credits_router.register(r'claims', ClaimViewSet, base_name='credits_claim')

urlpatterns = [
    path('', include(credits_router.urls)),
]
