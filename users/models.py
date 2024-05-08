from django.db import models


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(
        max_length=255, default=None, blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255, default=None, blank=True, null=True
    )
    email = models.EmailField()
    avatar_path = models.FilePathField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=50)
