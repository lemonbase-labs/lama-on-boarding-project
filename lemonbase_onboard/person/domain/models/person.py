import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class Person(AbstractUser):
    id = models.AutoField(primary_key=True)
    entity_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    registered_at = models.DateTimeField(auto_now_add=True, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=["entity_id"]),
        ]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
