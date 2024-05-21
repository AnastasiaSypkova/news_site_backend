from rest_framework import serializers

from posts_app.models import Posts


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for post model
    """

    class Meta:
        model = Posts
        exclude = [
            "author",
        ]
        extra_kwargs = {"comments_count": {"read_only": True}}

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
