from rest_framework import serializers

from person.models import Person


class BasicPersonDTO(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['email', 'name', 'registered_at']
