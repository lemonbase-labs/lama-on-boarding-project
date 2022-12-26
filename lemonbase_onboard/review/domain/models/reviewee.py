from django.db import models

from .review_cycle import ReviewCycle


class Reviewee(models.Model):
    id = models.AutoField(primary_key=True)
    review_cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE)
    person = models.ForeignKey(
        "person.Person", related_name="reviewees", on_delete=models.DO_NOTHING
    )
