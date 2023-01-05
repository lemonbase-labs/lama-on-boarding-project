import uuid

from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    entity_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    class Meta:
        indexes = [
            models.Index(fields=["entity_id"]),
        ]

    def update_question(self, title: str, description: str):
        self.title = title
        self.description = description

        self.save()
