from django.urls import include, path
from rest_framework import routers

from users_app.views import (
    GetUserByTokenView,
    MyTokenObtainPairView,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

signup_user = UserViewSet.as_view({"post": "create"})
urlpatterns = [
    path("auth/signup", signup_user, name="sign_up_user"),
    path(
        "auth/login/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("auth/whoami/", GetUserByTokenView.as_view(), name="whoami"),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path("", include(router.urls)),
]
