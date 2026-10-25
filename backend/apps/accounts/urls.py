from django.urls import path
from apps.accounts.views import UserListView, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),

    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("profile/", ProfileView.as_view(), name="my-profile"),
]