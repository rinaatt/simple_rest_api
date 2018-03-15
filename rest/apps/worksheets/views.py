import logging
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from apps.common.permissions import DjangoModelPermissionsWithRead
from .models import Worksheet
from .serializers import WorksheetSerializer

log = logging.getLogger('apps.common')


class WorksheetFilter(filters.FilterSet):
    min_created = filters.DateTimeFilter(name='created', lookup_expr='gte',
                                         label='Дата создания от')
    max_created = filters.DateTimeFilter(name='created', lookup_expr='lte',
                                         label='Дата создания до')
    min_birth_date = filters.DateFilter(name='birth_date', lookup_expr='gte',
                                        label='Дата рождения от')
    max_birth_date = filters.DateFilter(name='birth_date', lookup_expr='lte',
                                        label='Дата рождения до')
    min_score = filters.NumberFilter(name='score', lookup_expr='gte',
                                     label='Минимальный скоринговый балл')
    max_score = filters.NumberFilter(name='score', lookup_expr='lte',
                                     label='Максимальный скоринговый балл')

    class Meta:
        model = Worksheet
        fields = ('min_created', 'max_created',
                  'min_birth_date', 'max_birth_date',
                  'min_score', 'max_score', )


class WorksheetViewSet(viewsets.ModelViewSet):
    queryset = Worksheet.objects.all().order_by('created')
    serializer_class = WorksheetSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, )
    search_fields = ('surname', 'first_name', 'patronymic', 'phone_num')
    filter_class = WorksheetFilter
    permission_classes = (DjangoModelPermissionsWithRead, )
