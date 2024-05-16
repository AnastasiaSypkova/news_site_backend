from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import ReadOnly
from users_app.models import Users
from users_app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
