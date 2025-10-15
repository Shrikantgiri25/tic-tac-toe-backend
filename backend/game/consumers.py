import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Game, Move
from .game_logic import TicTacToeLogic

logger = logging.getLogger(__name__)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        # Authenticate user from JWT token in query string
        query_string = self.scope['query_string'].decode()
        token = query_string.split('token=')[1] if 'token=' in query_string else None

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                User = get_user_model()
                self.scope['user'] = await database_sync_to_async(User.objects.get)(id=user_id)
                logger.info(f"WebSocket authenticated user: {self.scope['user'].username}")
            except (InvalidToken, TokenError) as e:
                logger.warning(f"Invalid JWT token in WebSocket connection: {e}")
                await self.close()
                return
            except User.DoesNotExist as e:
                logger.warning(f"User not found for JWT token: {e}")
                await self.close()
                return
        else:
            logger.warning("No JWT token provided in WebSocket connection")
            self.scope['user'] = self.scope.get('user', None)

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

        # Send current game state
        game_state = await self.get_game_state()
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'game': game_state
        }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'make_move':
            await self.handle_move(data)
    
    async def handle_move(self, data):
        position = data.get('position')
        user = self.scope['user']

        logger.info(f"Move attempt by user {user.username} (ID: {user.id}) at position {position}")

        if not user or not user.is_authenticated:
            logger.warning(f"Unauthenticated move attempt from user: {user}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Not authenticated'
            }))
            return

        # Validate and process move
        result = await self.process_move(user, position)

        if result['success']:
            logger.info(f"Move successful for game {self.game_id}, broadcasting to group {self.game_group_name}")
            # Broadcast to all players in game
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_update',
                    'game': result['game_state']
                }
            )
        else:
            logger.warning(f"Move failed for game {self.game_id}: {result['error']}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': result['error']
            }))
    
    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'game': event['game']
        }))
    
    @database_sync_to_async
    def get_game_state(self):
        try:
            game = Game.objects.select_related(
                'player1', 'player2', 'current_turn', 'winner'
            ).get(id=self.game_id)
            
            return {
                'id': str(game.id),
                'player1': {
                    'id': str(game.player1.id),
                    'username': game.player1.username,
                    'symbol': 'X'
                },
                'player2': {
                    'id': str(game.player2.id),
                    'username': game.player2.username,
                    'symbol': 'O'
                } if game.player2 else None,
                'board_state': game.board_state,
                'current_turn': {
                    'id': str(game.current_turn.id),
                    'username': game.current_turn.username
                } if game.current_turn else None,
                'status': game.status,
                'winner': {
                    'id': str(game.winner.id),
                    'username': game.winner.username
                } if game.winner else None,
                'result': game.result
            }
        except Game.DoesNotExist:
            return None
    
    @database_sync_to_async
    def process_move(self, user, position):
        try:
            game = Game.objects.select_related('player1', 'player2', 'current_turn').get(
                id=self.game_id
            )

            logger.info(f"Processing move for game {game.id}, status: {game.status}")
            logger.debug(f"Current turn: {game.current_turn.username if game.current_turn else None} (ID: {game.current_turn.id if game.current_turn else None})")
            logger.debug(f"User attempting move: {user.username} (ID: {user.id})")

            # Validate game state
            if game.status != 'in_progress':
                logger.warning(f"Move attempted on game {game.id} with status: {game.status}")
                return {'success': False, 'error': 'Game is not in progress'}

            # FIX: Compare UUIDs directly, not as strings
            if game.current_turn is None or game.current_turn.id != user.id:
                logger.warning(f"Turn validation failed for game {game.id}: current_turn.id ({game.current_turn.id if game.current_turn else None}) != user.id ({user.id})")
                return {'success': False, 'error': 'Not your turn'}

            # Validate move
            row, col = TicTacToeLogic.position_to_coords(position)
            if not TicTacToeLogic.is_valid_move(game.board_state, row, col):
                return {'success': False, 'error': 'Invalid move'}

            # Determine player symbol
            symbol = 'X' if user == game.player1 else 'O'
            logger.info(f"Player {user.username} making move with symbol {symbol} at position {position} (row {row}, col {col})")

            # Make move
            game.board_state[row][col] = symbol
            logger.debug(f"Board after move: {game.board_state}")

            # Record move
            move_count = game.moves.count()
            Move.objects.create(
                game=game,
                player=user,
                position=position,
                move_number=move_count + 1
            )

            # Check for winner
            winner_symbol = TicTacToeLogic.check_winner(game.board_state)
            if winner_symbol:
                game.status = 'finished'
                game.winner = game.player1 if winner_symbol == 'X' else game.player2
                game.result = 'player1_win' if winner_symbol == 'X' else 'player2_win'
                game.finished_at = timezone.now()

                # Update stats
                game.winner.wins += 1
                game.winner.rating += 25
                game.winner.save()

                loser = game.player2 if winner_symbol == 'X' else game.player1
                loser.losses += 1
                loser.rating = max(0, loser.rating - 15)
                loser.save()

            elif TicTacToeLogic.is_board_full(game.board_state):
                game.status = 'finished'
                game.result = 'draw'
                game.finished_at = timezone.now()

                # Update stats
                game.player1.draws += 1
                game.player2.draws += 1
                game.player1.rating += 5
                game.player2.rating += 5
                game.player1.save()
                game.player2.save()
            else:
                # Switch turn
                old_turn = game.current_turn
                game.current_turn = game.player2 if user == game.player1 else game.player1
                logger.info(f"Turn switched from {old_turn.username} to {game.current_turn.username}")

            game.save()

            # FIX: Call the sync helper method instead of async one
            game_state = self._build_game_state(game)
            logger.debug(f"Returning game state for game {game.id}")
            return {
                'success': True,
                'game_state': game_state
            }

        except Game.DoesNotExist:
            logger.error(f"Game not found: {self.game_id}")
            return {'success': False, 'error': 'Game not found'}
        except Exception as e:
            logger.error(f"Exception in process_move for game {self.game_id}: {e}", exc_info=True)
            return {'success': False, 'error': 'Internal server error'}

    def _build_game_state(self, game):
        """Helper method to build game state dict (not async)"""
        return {
            'id': str(game.id),
            'player1': {
                'id': str(game.player1.id),
                'username': game.player1.username,
                'symbol': 'X'
            },
            'player2': {
                'id': str(game.player2.id),
                'username': game.player2.username,
                'symbol': 'O'
            } if game.player2 else None,
            'board_state': game.board_state,
            'current_turn': {
                'id': str(game.current_turn.id),
                'username': game.current_turn.username
            } if game.current_turn else None,
            'status': game.status,
            'winner': {
                'id': str(game.winner.id),
                'username': game.winner.username
            } if game.winner else None,
            'result': game.result
        }