from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    passport = serializers.CharField(max_length=12, label='Паспорт')
    owner = serializers.StringRelatedField()

    class Meta:
        model = Questionnaire
        fields = ('url', 'created', 'updated', 'surname', 'first_name',
                  'patronymic', 'birth_date', 'phone_num', 'passport',
                  'score', 'owner')
        read_only_fields = ('created', 'updated', 'owner')
