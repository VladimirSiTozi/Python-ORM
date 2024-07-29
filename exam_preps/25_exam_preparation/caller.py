import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Q, Count

# Create queries within functions

# 3.	Custom Model Manager

# print(TennisPlayer.objects.get_tennis_players_by_wins_count())

# 4.	Django Queries I

def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query = Q(query_name, query_country)
    elif search_name is not None:
        query = query_name
    else:
        query = query_country

    tennis_players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not tennis_players.exists():
        return ''

    result = [f'Tennis Player: {tp.full_name}, country: {tp.country}, ranking: {tp.ranking}' for tp in tennis_players]

    return '\n'.join(result)

# print(get_tennis_players(None, 'Spain'))


def get_top_tennis_player():
    top_tennis_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_tennis_player:
        return f"Top Tennis Player: {top_tennis_player.full_name} with {top_tennis_player.wins_count} wins."
    return ''

# print(get_top_tennis_player())


def get_tennis_player_by_matches_count():
    most_matches_tennis_player = (TennisPlayer.objects.annotate(matches_count=Count('player_matches'))
                                  .order_by('-matches_count', 'ranking')
                                  .first()
                                  )
    if not Match.objects.all():
        return ''

    if most_matches_tennis_player:
        return (f"Tennis Player: {most_matches_tennis_player.full_name} "
                f"with {most_matches_tennis_player.matches_count} matches played.")
    return ''

# print(get_tennis_player_by_matches_count())


# 5.	Django Queries II

def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = (Tournament.objects.annotate(matches_count=Count('tournament_matches'))
                   .filter(surface_type__icontains=surface)
                   .order_by('-start_date')
                   )

    if not tournaments:
        return ''

    # !
    # if not Tournament.objects.all().exists():
    #     return ''

    result = [f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}' for t in tournaments]

    return '\n'.join(result)

# print(get_tournaments_by_surface_type('Clay'))


def get_latest_match_info():
    last_match = (Match.objects.prefetch_related('players', 'winner')
                  .order_by('-date_played', '-id')
                  .first()
                  )

    if not last_match:
        return ''

    players = [p.full_name for p in last_match.players.order_by('full_name').all()]

    winner_name = 'TBA' if last_match.winner is None else last_match.winner.full_name

    return (f"Latest match played on: {last_match.date_played}, tournament: {last_match.tournament.name}, "
            f"score: {last_match.score}, players: {players[0]} vs {players[1]}, "
            f"winner: {winner_name}, "
            f"summary: {last_match.summary}")

# print(get_latest_match_info())


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    if not Tournament.objects.filter(name=tournament_name):
        return "No matches found."

    matches = (Match.objects.filter(tournament__name=tournament_name)
               .order_by('-date_played')
               )

    if not matches:
        return "No matches found."

    result = []

    for m in matches:
        winner_name = "TBA" if m.winner is None else m.winner.full_name
        result.append(f'Match played on: {m.date_played}, score: {m.score}, '
                      f'winner: {winner_name}')

    return '\n'.join(result)


print(get_matches_by_tournament('Roland Garros'))

