from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import ReadOnly
from users.models import Users
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
