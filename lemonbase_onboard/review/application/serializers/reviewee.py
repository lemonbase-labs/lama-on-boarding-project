from rest_framework import serializers

from review.models import Reviewee
from person.application.serializers.basic_person import BasicPersonSerializer


class RevieweeSerializer(serializers.ModelSerializer):
    entity_id = serializers.UUIDField()
    person = BasicPersonSerializer

    class Meta:
        model = Reviewee
        fields = ['entity_id', 'person']
