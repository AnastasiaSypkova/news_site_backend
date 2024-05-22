from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from news_site_backend.permissions import EditeOwnPost, ReadOnly
from posts_app.models import Posts
from posts_app.serializers import PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with posts model

    Only authenticated users can add news
    All users can read news
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | ReadOnly, EditeOwnPost | ReadOnly]

    def get_queryset(self):
        """
        implement filtering against query set parameters

        Filtering by author id, author first and last name,
        author email, and text to search in post title and post text
        """
        queryset = Posts.objects.all()
        author = self.request.query_params.get("author")
        author_query_id = self.request.query_params.get("authorId")
        email = self.request.query_params.get("email")
        if author:
            queryset = queryset.filter(author__first_name=author)
            if not queryset:
                queryset = queryset.filter(author__last_name=author)
        if author_query_id:
            queryset = queryset.filter(author_id=author_query_id)
        if email:
            queryset = queryset.filter(author__email=email)

        return queryset
