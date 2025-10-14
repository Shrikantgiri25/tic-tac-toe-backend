from django.db import models
from django.conf import settings
import uuid

class Game(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Player'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    
    RESULT_CHOICES = [
        ('player1_win', 'Player 1 Win'),
        ('player2_win', 'Player 2 Win'),
        ('draw', 'Draw'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player1 = models.ForeignKey("accounts.User", on_delete=models.CASCADE, 
                                related_name='games_as_player1')
    player2 = models.ForeignKey("accounts.User", on_delete=models.CASCADE, 
                                related_name='games_as_player2', null=True, blank=True)
    board_state = models.JSONField(default=list)
    current_turn = models.ForeignKey("accounts.User", on_delete=models.CASCADE,
                                     related_name='current_turn_games', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    winner = models.ForeignKey("accounts.User", on_delete=models.CASCADE,
                               related_name='won_games', null=True, blank=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def initialize_board(self):
    # just initialize the list; save later
        self.board_state = [[None, None, None] for _ in range(3)]


class Move(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.IntegerField()
    move_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['move_number']