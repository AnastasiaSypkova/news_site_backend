from rest_framework import serializers

from users_app.models import MyUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar_path",
            "email",
            "password",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}
