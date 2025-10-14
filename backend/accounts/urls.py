from django.urls import path
from .views import RegisterView, CurrentUserView, LeaderboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
