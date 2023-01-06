from rest_framework import serializers

from person.models import Person


class BasicPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['entity_id', 'email', 'name', 'registered_at']
