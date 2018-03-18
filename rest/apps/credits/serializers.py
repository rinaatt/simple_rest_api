from rest_framework import serializers
from .models import Claim


class ClaimSerializer(serializers.HyperlinkedModelSerializer):
    offer = serializers.StringRelatedField()
    questionnaire = serializers.StringRelatedField()

    class Meta:
        model = Claim
        fields = ('url', 'created', 'sent', 'questionnaire', 'offer', 'status')
        read_only_fields = ('created', 'sent', 'status', )
