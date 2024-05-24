from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from comments_app.models import Comments
from comments_app.serializers import CommentsSerializer
from news_site_backend.permissions import EditeOwnObject, ReadOnly


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints assotiated with comments model

    Only authenticated users can write and read comments
    """

    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
    permission_classes = [IsAuthenticated, EditeOwnObject | ReadOnly]
