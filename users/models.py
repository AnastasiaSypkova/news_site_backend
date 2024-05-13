from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_to(instance, filename):
    return "/".join(["images", str(instance.avatar_path), filename])


class Users(AbstractUser):
    avatar_path = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        ordering = ["id"]
