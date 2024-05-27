from django.urls import include, path
from rest_framework import routers

from comments_app.views import CommentsViewSet

router = routers.DefaultRouter()
router.register("", CommentsViewSet, basename="comments")

urlpatterns = [path("", include(router.urls))]
