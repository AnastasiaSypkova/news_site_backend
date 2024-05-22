from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import EditeOwnPost, ReadOnly
from posts_app.models import Posts
from posts_app.serializers import PostSerializer


class CustomFilterBackend(filters.BaseFilterBackend):
    """
    implement filtering against query set parameters

    Filtering by author id, author first and last name,
    author email, and text to search in post title and post text
    """

    def filter_queryset(self, request, queryset, view):
        queryset = Posts.objects.all()
        author = request.query_params.get("author")
        author_query_id = request.query_params.get("authorId")
        if author:
            queryset = queryset.filter(author__first_name=author)
            if not queryset:
                queryset = Posts.objects.all().filter(author__last_name=author)
            if not queryset:
                queryset = Posts.objects.all().filter(author__email=author)
        if author_query_id:
            queryset = queryset.filter(author_id=author_query_id)

        return queryset


class PostsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with posts model

    Only authenticated users can add news
    All users can read news
    """

    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = [IsAuthenticated | ReadOnly, EditeOwnPost | ReadOnly]
    filter_backends = [
        CustomFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "text"]
    ordering_fields = ["created_at"]
    filterset_fields = ["author"]
    ordering = ["created_at"]
