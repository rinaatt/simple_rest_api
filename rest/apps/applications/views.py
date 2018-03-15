from rest_framework import viewsets, permissions
from .models import Application
from .serializers import ApplicationSerializer

permissions.BasePermission()


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('created')
    serializer_class = ApplicationSerializer
