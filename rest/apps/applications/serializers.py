from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    offer = serializers.StringRelatedField()
    questionnaire = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ('url', 'created', 'sent', 'questionnaire', 'offer', 'status')
        read_only_fields = ('created', 'sent', 'status', )
