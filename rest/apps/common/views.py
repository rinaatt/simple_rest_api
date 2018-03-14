import logging
from rest_framework import viewsets
from .models import Organization
from .serializers import OrganizationSerializer

log = logging.getLogger('apps.common')


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by('name')
    serializer_class = OrganizationSerializer
