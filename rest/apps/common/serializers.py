from .models import Offer, Organization
from rest_framework import serializers


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ('url', 'name', )


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Offer
        fields = ('created', 'updated', 'rotation_start', 'rotation_finish',
                  'name', 'typ', 'min_score', 'max_score', 'organization')
        read_only_fields = ('created', 'updated', )
