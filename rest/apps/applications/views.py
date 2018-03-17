from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from apps.common.permissions import DjangoModelPermissionsWithRead
from django.contrib.auth.models import User
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (DjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        user: User = self.request.user
        if not user.has_perm('applications.read_application'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset
