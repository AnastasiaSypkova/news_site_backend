from rest_framework import serializers, viewsets

from users.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
