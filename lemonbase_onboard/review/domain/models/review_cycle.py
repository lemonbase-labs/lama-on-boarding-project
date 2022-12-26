from django.db import models

from person.models import Person
from review.domain.models.question import Question


class ReviewCycle(models.Model):
    id = models.AutoField(primary_key=True)
    review_cycle_creator = models.ForeignKey(
        Person, related_name="review_cycles", on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=128)
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
    )
