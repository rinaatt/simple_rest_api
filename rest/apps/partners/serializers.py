from rest_framework import serializers
from apps.questionnaires.models import Questionnaire
from apps.claims.models import Claim


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    passport = serializers.CharField(max_length=12, label='Паспорт')
    owner = serializers.StringRelatedField()

    class Meta:
        model = Questionnaire
        fields = ('url', 'created', 'updated', 'surname', 'first_name',
                  'patronymic', 'birth_date', 'phone_num', 'passport',
                  'score', 'owner')
        read_only_fields = ('created', 'updated', 'owner')


class ClaimSerializer(serializers.ModelSerializer):
    offer = serializers.StringRelatedField()
    questionnaire = serializers.StringRelatedField()

    class Meta:
        model = Claim
        fields = ('created', 'sent', 'questionnaire', 'offer', 'status')
        read_only_fields = ('created', 'sent', 'status', )
