from rest_framework import serializers
from apps.partners.models import Questionnaire
from apps.credits.models import Claim


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    passport = serializers.CharField(max_length=12, label='Паспорт')

    class Meta:
        model = Questionnaire
        fields = ('url', 'created', 'updated', 'surname', 'first_name',
                  'patronymic', 'birth_date', 'phone_num', 'passport',
                  'score')


class QuestionnaireRelatedField(serializers.PrimaryKeyRelatedField):

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return Questionnaire.objects.get(pk=data)
        except Questionnaire.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def get_queryset(self):
        request = self.context['request']
        organization = getattr(request.user, 'organization', None)
        return Questionnaire.objects.filter(organization=organization)

    def display_value(self, instance):
        return instance.full_name


class ClaimSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireRelatedField(label='Анкета')

    class Meta:
        model = Claim
        fields = ('created', 'sent', 'questionnaire', 'questionnaire_display',
                  'offer', 'offer_dispaly', 'status_display')
        read_only_fields = ('sent', 'questionnaire_display', 'offer_dispaly',
                            'status_display', )
