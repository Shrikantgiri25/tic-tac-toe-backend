from django.urls import path
from .views import CreateGameView, JoinMatchmakingView, GameDetailView, MyGamesView

app_name = "game"

urlpatterns = [
    path("create/", CreateGameView.as_view(), name="create-game"),
    path("matchmaking/", JoinMatchmakingView.as_view(), name="join-matchmaking"),
    path("<uuid:game_id>/", GameDetailView.as_view(), name="game-detail"),
    path("my/", MyGamesView.as_view(), name="my-games"),
]
