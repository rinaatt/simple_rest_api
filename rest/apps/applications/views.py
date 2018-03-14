from rest_framework import viewsets
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('created')
    serializer_class = ApplicationSerializer
