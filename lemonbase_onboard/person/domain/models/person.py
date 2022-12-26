from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    registered_at = models.DateTimeField(auto_now_add=True)
