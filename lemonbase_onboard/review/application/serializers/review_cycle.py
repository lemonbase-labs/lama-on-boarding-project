from rest_framework import serializers

from review.application.serializers.reviewee import RevieweeSerializer
from person.application.serializers.basic_person import BasicPersonSerializer
from review.application.serializers.review_cycle_question import (
    ReviewCycleQuestionSerializer,
)
from review.models import ReviewCycle


class ReviewCycleSerializer(serializers.ModelSerializer):
    entity_id = serializers.UUIDField()
    creator = BasicPersonSerializer
    question = ReviewCycleQuestionSerializer
    reviewees = RevieweeSerializer(many=True)

    class Meta:
        model = ReviewCycle
        fields = ["entity_id", "name", "creator", "question", "reviewees"]
