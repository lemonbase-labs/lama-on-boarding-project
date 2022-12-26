from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
