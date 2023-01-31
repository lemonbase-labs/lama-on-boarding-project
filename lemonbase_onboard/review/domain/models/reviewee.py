import uuid

from django.db import models

from review.domain.models.review_cycle import ReviewCycle


class Reviewee(models.Model):
    id = models.AutoField(primary_key=True)
    entity_id = models.UUIDField(default=uuid.uuid4, editable=False)
    review_cycle = models.ForeignKey(
        ReviewCycle, on_delete=models.CASCADE, related_name="reviewees"
    )
    person = models.ForeignKey(
        "person.Person", related_name="assigned_reviewees", on_delete=models.DO_NOTHING
    )

    class Meta:
        indexes = [
            models.Index(fields=["entity_id"]),
        ]
