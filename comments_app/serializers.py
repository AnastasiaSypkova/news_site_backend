from rest_framework import serializers

from comments_app.models import Comments
from posts_app.models import Posts
from users_app.serializers import UserSerializer


class CommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for comments model
    """

    post_id = serializers.PrimaryKeyRelatedField(
        source="post", queryset=Posts.objects.all()
    )
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        source="author", read_only=True
    )

    class Meta:
        model = Comments
        exclude = ["post"]
        extra_kwargs = {
            "author": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
