from rest_framework import serializers
from .models import Game, Move
from accounts.serializers.user_serializer import UserSerializer

class MoveSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)
    
    class Meta:
        model = Move
        fields = ['id', 'player', 'position', 'move_number', 'created_at']

class GameSerializer(serializers.ModelSerializer):
    player1 = UserSerializer(read_only=True)
    player2 = UserSerializer(read_only=True)
    current_turn = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    moves = MoveSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'board_state', 'current_turn',
                  'status', 'winner', 'result', 'created_at', 'updated_at',
                  'finished_at', 'moves']