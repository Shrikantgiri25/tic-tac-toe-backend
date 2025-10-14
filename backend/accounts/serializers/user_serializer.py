from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    total_games = serializers.IntegerField(read_only=True)
    win_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'wins', 'losses', 'draws', 'rating', 
                  'total_games', 'win_rate']
        read_only_fields = ['id', 'wins', 'losses', 'draws', 'rating']
