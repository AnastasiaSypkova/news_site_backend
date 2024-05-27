from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users_app.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user model
    """

    rating = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = MyUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar_path",
            "email",
            "password",
            "rating",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def to_representation(self, instance):
        """
        Make image file path relative
        """
        response = super(UserSerializer, self).to_representation(instance)
        if instance.avatar_path:
            response["avatar_path"] = instance.avatar_path.url
        return response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for custom token response

    It returns access token, refresh token and user data
    """

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        data.update({"user": UserSerializer(self.user).data})

        return data
