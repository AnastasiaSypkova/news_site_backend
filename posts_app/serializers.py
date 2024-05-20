from rest_framework import serializers

from posts_app.models import Posts


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for post model
    """

    class Meta:
        model = Posts
        fields = "__all__"
