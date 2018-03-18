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
    # search_fields = ('surname', 'first_name', 'patronymic', 'phone_num')
    ordering = ('created', )
    filter_class = QuestionnaireFilter
    permission_classes = (IsOwnerOrDjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        user: User = self.request.user
        if not user.has_perm('questionnaires.read_questionnaire'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        setattr(self, '_ignore_model_permissions', True)
        return super().retrieve(request, *args, **kwargs)


class ClaimViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (DjangoModelPermissions, )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)
