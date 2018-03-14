import logging
from rest_framework import viewsets
from .models import Organization, Offer
from .serializers import OrganizationSerializer, OfferSerializer

log = logging.getLogger('apps.common')


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by('name')
    serializer_class = OrganizationSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('created')
    serializer_class = OfferSerializer
