from rest_framework import serializers

from review.models import Question


class ReviewCycleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["title", "description"]
