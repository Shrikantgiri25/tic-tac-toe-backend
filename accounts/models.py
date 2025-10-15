from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    rating = models.IntegerField(default=1000)
    
    class Meta:
        ordering = ['-rating']
    
    @property
    def total_games(self):
        return self.wins + self.losses + self.draws
    
    @property
    def win_rate(self):
        if self.total_games == 0:
            return 0
        return round((self.wins / self.total_games) * 100, 2)