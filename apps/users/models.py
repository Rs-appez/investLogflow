from typing import override
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = "users"

    @override
    def __str__(self):
        return self.username


class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="organizations")

    @override
    def __str__(self):
        return self.name
