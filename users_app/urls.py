from django.urls import include, path
from rest_framework import routers

from users_app.views import (
    GetUserByTokenView,
    MyTokenObtainPairView,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register("", UserViewSet)

signup_user = UserViewSet.as_view({"post": "create"})
urlpatterns = [
    path("signup/", signup_user, name="sign_up_user"),
    path(
        "login/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("whoami/", GetUserByTokenView.as_view(), name="whoami"),
    path("", include(router.urls)),
]
