import logging
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import User
from apps.common.permissions import IsOwnerOrDjangoModelPermissions
from apps.credits.models import Claim
from apps.partners.models import Questionnaire
from .serializers import QuestionnaireSerializer, ClaimSerializer
from .filters import QuestionnaireFilter

log = logging.getLogger('apps.partners')


class QuestionnaireViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()
    ordering = ('created', )
    filter_class = QuestionnaireFilter
    permission_classes = (IsOwnerOrDjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        # user: User = self.request.user
        queryset = queryset.filter(organization=self.request.user.organization)
        return queryset

    # def retrieve(self, request, *args, **kwargs):
    #     setattr(self, '_ignore_model_permissions', True)
    #     return super().retrieve(request, *args, **kwargs)


class ClaimViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (DjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = getattr(self.request.user, 'organization', None)
        return queryset.filter(partner=organization)

    def perform_create(self, serializer):
        organization = getattr(self.request.user, 'organization', None)
        serializer.save(partner=organization)
