from rest_framework import serializers

from review.models import Question


class ReviewCycleQuestionDTO(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']
