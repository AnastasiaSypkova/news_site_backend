from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from news_site_backend.permissions import ReadOnly, UpdateOwnProfile
from users_app.models import MyUser
from users_app.serializers import MyTokenObtainPairSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for endpoints assotiated with user model"""

    queryset = MyUser.objects.annotate(
        rating=Coalesce(Avg("posts__rating"), Value(0.0))
    )
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated | ReadOnly,
        UpdateOwnProfile | ReadOnly,
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data, "total": len(queryset)})


class MyTokenObtainPairView(TokenObtainPairView):
    """View for auth/login endpoint

    Get email and password
    Returns refresh, access tokens and user data
    """

    serializer_class = MyTokenObtainPairSerializer


class GetUserByTokenView(generics.ListAPIView):
    """View for whoami endpoint

    Get access token returns current user
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        if self.request.user.id:
            queryset = MyUser.objects.get(id=self.request.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
