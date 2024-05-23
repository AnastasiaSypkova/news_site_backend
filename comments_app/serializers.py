from rest_framework import serializers

from comments_app.models import Comments
from posts_app.models import Posts


class CommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for comments model
    """

    post_id = serializers.PrimaryKeyRelatedField(
        source="post", queryset=Posts.objects.all(), write_only=True
    )

    class Meta:
        model = Comments
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "post": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
