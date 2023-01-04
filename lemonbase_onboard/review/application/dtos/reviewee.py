from rest_framework import serializers

from review.models import Reviewee
from person.application.dtos.basic_person import BasicPersonDTO


class RevieweeDTO(serializers.ModelSerializer):
    entity_id = serializers.UUIDField()
    person = BasicPersonDTO

    class Meta:
        model = Reviewee
        fields = ['entity_id', 'person']
