import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    id = models.AutoField(primary_key=True)
    entity_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
