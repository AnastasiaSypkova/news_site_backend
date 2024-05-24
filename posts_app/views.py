from django.db.models import Count
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from news_site_backend.permissions import EditeOwnObject, ReadOnly
from posts_app.models import Posts
from posts_app.serializers import PostSerializer


class CustomFilterBackend(filters.BaseFilterBackend):
    """
    implement filtering against query set parameters

    Filtering by author id, author first and last name,
    author email, tags and text to search in post title and post text
    """

    def filter_queryset(self, request, queryset, view):
        queryset_annotated = Posts.objects.annotate(
            comments_count=Count("comments")
        ).all()

        author = request.query_params.get("author")
        author_query_id = request.query_params.get("authorId")
        tags = request.query_params.get("tags")
        if author:
            queryset = queryset_annotated.filter(author__first_name=author)
            if not queryset:
                queryset = queryset_annotated.filter(author__last_name=author)
            if not queryset:
                queryset = queryset_annotated.filter(author__email=author)
        if author_query_id:
            queryset = queryset.filter(author_id=author_query_id)
        if tags:
            tags = tags.split()
            for tag in tags:
                queryset = queryset.filter(tags__icontains=tag)

        return queryset


class PostsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with posts model

    Only authenticated users can add news
    All users can read news
    """

    serializer_class = PostSerializer
    queryset = Posts.objects.annotate(comments_count=Count("comments")).all()
    permission_classes = [
        IsAuthenticated | ReadOnly,
        EditeOwnObject | ReadOnly,
    ]
    filter_backends = [
        CustomFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "text"]
    ordering_fields = ["created_at"]
    filterset_fields = ["author"]
    ordering = ["created_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"posts": serializer.data, "total": len(queryset)})
