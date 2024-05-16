from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users_app.models import Users


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = Users
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
