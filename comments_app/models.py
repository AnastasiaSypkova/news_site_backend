from django.db import models

from posts_app.models import Posts
from users_app.models import MyUser


class Comments(models.Model):
    """
    Model for comments wriiten by user to specific post
    """

    text = models.CharField(max_length=255)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
