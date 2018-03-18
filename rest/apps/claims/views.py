from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from apps.common.permissions import DjangoModelPermissionsWithRead
from django.contrib.auth.models import User
from .models import Claim
from .serializers import ClaimSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (DjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        user: User = self.request.user
        if not user.has_perm('claims.read_claim'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset
