from rest_framework import serializers
from .models import Worksheet


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):
    passport = serializers.CharField(max_length=12, label='Паспорт')

    class Meta:
        model = Worksheet
        fields = ('url', 'created', 'updated', 'surname', 'first_name',
                  'patronymic', 'birth_date', 'phone_num', 'passport',
                  'score', )
        read_only_fields = ('created', 'updated', )
