from django.urls import include, path
from rest_framework import routers

from posts_app.views import PostsViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostsViewSet)

urlpatterns = [path("", include(router.urls))]
