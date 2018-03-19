from django_filters import rest_framework as filters
from apps.credits.models import Claim


class ClaimFilter(filters.FilterSet):
    min_created = filters.DateTimeFilter(name='created', lookup_expr='gte',
                                         label='Дата создания от')
    max_created = filters.DateTimeFilter(name='created', lookup_expr='lte',
                                         label='Дата создания до')
    min_sent = filters.DateFilter(name='sent', lookup_expr='gte',
                                  label='Дата просмотра от')
    max_sent = filters.DateFilter(name='sent', lookup_expr='lte',
                                  label='Дата просмотра до')
    order = filters.OrderingFilter(
        fields=(
            ('questionnaire', 'questionnaire'),
            ('created', 'created'),
            ('sent', 'sent'),
        ),
        field_labels={
            'questionnaire': 'По анкете',
            'created': 'По дате создания ',
            'sent': 'По дате просмотра'
        }
    )

    class Meta:
        model = Claim
        fields = ('min_created', 'max_created', 'min_sent', 'max_sent', )
