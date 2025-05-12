# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.username
