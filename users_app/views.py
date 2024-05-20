from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import ReadOnly, UpdateOwnProfile
from users_app.models import MyUser
from users_app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated | ReadOnly,
        UpdateOwnProfile | ReadOnly,
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return super().get_permissions()
