from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from .models import Game
from .serializer import GameSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


def create_game_for_user(user):
    """Helper: Create and initialize a new game for the given user"""
    game = Game.objects.create(player1=user, status='waiting')
    game.initialize_board()
    game.save()
    return game


class CreateGameView(APIView):
    """Create a new game and wait for opponent"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Create a new game",
        description="Create a new Tic Tac Toe game. If user already has an active game, returns that game instead.",
        responses={
            200: GameSerializer,
            201: GameSerializer,
            401: {"description": "Unauthorized"}
        },
        tags=['Games']
    )
    def post(self, request):
        try:
            # Check if user already has an active or waiting game
            active_game = Game.objects.filter(
                Q(player1=request.user) | Q(player2=request.user),
                status__in=['waiting', 'in_progress']
            ).first()

            if active_game:
                logger.info(f"[CreateGame] {request.user.username} already in game {active_game.id}")
                serializer = GameSerializer(active_game)
                return Response(serializer.data)

            # Otherwise create a new game
            game = create_game_for_user(request.user)
            logger.info(f"[CreateGame] New game created for {request.user.username}: {game.id}")
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating game for user {request.user.username}: {e}")
            return Response(
                {'error': 'Failed to create game'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JoinMatchmakingView(APIView):
    """Join matchmaking — find existing waiting game or create a new one"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Join matchmaking",
        description="Join matchmaking to find an opponent. Will join existing waiting game or create new one.",
        responses={
            200: GameSerializer,
            201: GameSerializer,
            401: {"description": "Unauthorized"}
        },
        tags=['Games']
    )
    def post(self, request):
        try:
            user = request.user

            # Check if user already in a game
            active_game = Game.objects.filter(
                Q(player1=user) | Q(player2=user),
                status__in=['waiting', 'in_progress']
            ).first()

            if active_game:
                logger.info(f"[JoinMatchmaking] {user.username} already in active game {active_game.id}")
                return Response(GameSerializer(active_game).data)

            # Try to join an existing waiting game
            waiting_game = Game.objects.filter(
                status='waiting',
                player2__isnull=True
            ).exclude(player1=user).first()

            if waiting_game:
                waiting_game.player2 = user
                waiting_game.current_turn = waiting_game.player1  # Player 1 (X) always starts
                waiting_game.status = 'in_progress'
                waiting_game.save()

                logger.info(f"[JoinMatchmaking] {user.username} joined game {waiting_game.id}")
                logger.info(f"[JoinMatchmaking] Current turn: {waiting_game.current_turn.username}")

                # Notify both players in WebSocket group
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'game_{waiting_game.id}',
                    {
                        'type': 'game_update',
                        'game': GameSerializer(waiting_game).data
                    }
                )

                return Response(GameSerializer(waiting_game).data)

            # No waiting game found → create a new one
            logger.info(f"[JoinMatchmaking] Creating new game for {user.username}")
            new_game = create_game_for_user(user)
            serializer = GameSerializer(new_game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in matchmaking for user {request.user.username}: {e}")
            return Response(
                {'error': 'Failed to join matchmaking'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GameDetailView(APIView):
    """Get details of a specific game"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get game details",
        description="Retrieve details of a specific game by ID.",
        parameters=[
            {
                'name': 'game_id',
                'type': 'string',
                'location': 'path',
                'description': 'UUID of the game'
            }
        ],
        responses={
            200: GameSerializer,
            401: {"description": "Unauthorized"},
            404: {"description": "Game not found"}
        },
        tags=['Games']
    )
    def get(self, request, game_id):
        try:
            game = get_object_or_404(Game, id=game_id)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving game {game_id}: {e}")
            return Response(
                {'error': 'Failed to retrieve game'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyGamesView(APIView):
    """List all games of the authenticated user"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get user's games",
        description="Retrieve all games (past and present) for the authenticated user.",
        responses={
            200: GameSerializer(many=True),
            401: {"description": "Unauthorized"}
        },
        tags=['Games']
    )
    def get(self, request):
        try:
            games = Game.objects.filter(
                Q(player1=request.user) | Q(player2=request.user)
            )
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving games for user {request.user.username}: {e}")
            return Response(
                {'error': 'Failed to retrieve games'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
