from django.db import models

from users_app.models import MyUser


def upload_cover(instanse, filename):
    """
    Defines path where to upload cover image for post
    """
    return "/".join(["cover_posts", str(instanse.cover_path), filename])


class Posts(models.Model):
    """
    Model for Posts
    """

    title = models.CharField(max_length=255)
    text = models.TextField(null=False, blank=False)
    cover_path = models.ImageField(
        upload_to=upload_cover, blank=False, null=False
    )
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=255)
