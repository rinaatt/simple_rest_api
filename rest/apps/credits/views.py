from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.utils import timezone
from .models import Claim
from .serializers import ClaimSerializer


class ClaimViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (DjangoModelPermissions, )

    def retrieve(self, request, *args, **kwargs):
        claim: Claim = self.get_object()
        if claim.sent is None:
            claim.sent = timezone.now()
            claim.status = Claim.SENT
            claim.save()
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = getattr(self.request.user, 'organization', None)
        if organization is not None:
            queryset = queryset.filter(offer__organization=organization)
        return queryset
