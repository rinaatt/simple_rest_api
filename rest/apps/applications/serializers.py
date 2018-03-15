from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    offer = serializers.StringRelatedField()
    worksheet = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ('url', 'created', 'sent', 'worksheet', 'offer', 'status')
        read_only_fields = ('created', 'sent', 'status', )
