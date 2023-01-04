from rest_framework import serializers

from review.application.dtos.reviewee import RevieweeDTO
from person.application.dtos.basic_person import BasicPersonDTO
from review.application.dtos.review_cycle_question import ReviewCycleQuestionDTO
from review.models import ReviewCycle


class ReviewCycleDTO(serializers.ModelSerializer):
    entity_id = serializers.UUIDField()
    creator = BasicPersonDTO
    question = ReviewCycleQuestionDTO
    reviewees = RevieweeDTO(many=True)

    class Meta:
        model = ReviewCycle
        fields = ['entity_id', 'name', 'creator', 'question', 'reviewees']
