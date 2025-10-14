import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Game, Move

User = get_user_model()


class GameAPITestCase(APITestCase):
    def setUp(self):
        """Set up test users and authentication"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

    def test_create_game(self):
        """Test creating a new game"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('game:create_game')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['player1']['username'], 'testuser1')
        self.assertEqual(response.data['status'], 'waiting')

    def test_join_matchmaking(self):
        """Test joining matchmaking"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('game:join_matchmaking')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game_id = response.data['id']

        # Second user joins
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], game_id)
        self.assertEqual(response.data['player2']['username'], 'testuser2')
        self.assertEqual(response.data['status'], 'in_progress')

    def test_get_game_detail(self):
        """Test retrieving game details"""
        # Create a game first
        self.client.force_authenticate(user=self.user1)
        create_url = reverse('game:create_game')
        create_response = self.client.post(create_url)
        game_id = create_response.data['id']

        # Get game details
        detail_url = reverse('game:game_detail', kwargs={'game_id': game_id})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], game_id)

    def test_get_my_games(self):
        """Test retrieving user's games"""
        # Create a game
        self.client.force_authenticate(user=self.user1)
        create_url = reverse('game:create_game')
        self.client.post(create_url)

        # Get user's games
        my_games_url = reverse('game:my_games')
        response = self.client.get(my_games_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_unauthorized_access(self):
        """Test that unauthenticated requests are rejected"""
        url = reverse('game:create_game')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GameModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='modeltest1',
            email='model1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='modeltest2',
            email='model2@example.com',
            password='testpass123'
        )

    def test_game_creation(self):
        """Test game model creation"""
        game = Game.objects.create(player1=self.user1)
        game.initialize_board()

        self.assertEqual(game.status, 'waiting')
        self.assertEqual(game.player1, self.user1)
        self.assertIsNone(game.player2)
        self.assertEqual(game.board_state, [[None, None, None], [None, None, None], [None, None, None]])

    def test_game_str_representation(self):
        """Test game string representation"""
        game = Game.objects.create(player1=self.user1)
        expected_str = f"Game {game.id}: {self.user1.username} vs None"
        self.assertEqual(str(game), expected_str)


class MoveModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='movetest1',
            email='move1@example.com',
            password='testpass123'
        )
        self.game = Game.objects.create(player1=self.user1)
        self.game.initialize_board()
        self.game.save()

    def test_move_creation(self):
        """Test move model creation"""
        move = Move.objects.create(
            game=self.game,
            player=self.user1,
            position=0,
            move_number=1
        )

        self.assertEqual(move.game, self.game)
        self.assertEqual(move.player, self.user1)
        self.assertEqual(move.position, 0)
        self.assertEqual(move.move_number, 1)
