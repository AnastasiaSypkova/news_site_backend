from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

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
        post_id = request.query_params.get("post")
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
