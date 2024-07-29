from django.db import models
from django.db.models import Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        players = self.annotate(wins_count=Count('player_wins')).order_by('-wins_count', 'full_name')
        return players
