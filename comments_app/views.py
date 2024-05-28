from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments_app.models import Comments
from comments_app.serializers import CommentsSerializer
from news_site_backend.permissions import EditeOwnObject, ReadOnly


class FilterByPostIdBackend(filters.BaseFilterBackend):
    """
    implement filtering against query set parameters

    Filtering comments by post id
    """

    def filter_queryset(self, request, queryset, view):
        queryset = Comments.objects.all()
        post_id = request.query_params.get("postId")
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with comments model

    Only authenticated users can write and read comments
    """

    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    permission_classes = [IsAuthenticated, EditeOwnObject | ReadOnly]
    filter_backends = [FilterByPostIdBackend]
    filterset_fields = ["post"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({"results": serializer.data, "total": len(queryset)})
