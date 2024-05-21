from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import ReadOnly
from posts_app.models import Posts
from posts_app.serializers import PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with posts model

    Only authenticated users can add news
    All users can read news
    """

    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)
