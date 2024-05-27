from rest_framework import serializers

from posts_app.models import Posts
from users_app.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for post model
    """

    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True
    )
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source="author", read_only=True
    )

    class Meta:
        model = Posts
        fields = "__all__"

        extra_kwargs = {
            "comments_count": {"read_only": True},
            "author": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Make image file path relative
        """
        response = super(PostSerializer, self).to_representation(instance)
        if instance.cover_path:
            response["cover_path"] = instance.cover_path.url
        if instance.author.avatar_path:
            response["author"]["avatar_path"] = instance.author.avatar_path.url
        return response
