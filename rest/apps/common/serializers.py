from .models import Offer, Organization
from rest_framework import serializers


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    organization = serializers.StringRelatedField()

    class Meta:
        model = Offer
        fields = ('created', 'updated', 'rotation_start', 'rotation_finish',
                  'name', 'organization', 'type', 'min_score', 'max_score', )
        read_only_fields = ('created', 'updated', )
