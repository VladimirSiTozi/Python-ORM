import os
from decimal import Decimal
from math import ceil
from random import randint

import django
from django.db.models import Count, Sum, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import FootballPlayer, FootballCoach, Team, League
from populate_db import populate_func

# Create queries within functions

# Create players, coaches and teams
# print(populate_func())


# Populate all info for teams, player and coaches

def give_all_clubs_a_name_coach_and_league():
    teams_mapping = {
        1: 'Arsenal',
        2: 'Aston Villa',
        3: 'Bournemouth',
        4: 'Brentford',
        5: 'Brighton',
        6: 'Burnley',
        7: 'Chelsea',
        8: 'Crystal Palace',
        9: 'Everton',
        10: 'Fulham',
        11: 'Liverpool',
        12: 'Luton Town',
        13: 'Manchester City',
        14: 'Manchester United',
        15: 'Newcastle United',
        16: 'Nottingham Forest',
        17: 'Sheffield United',
        18: 'Tottenham Hotspur',
        19: 'West Ham United',
        20: 'Wolverhampton Wanderers',
        21: 'Birmingham City',
        22: 'Blackburn Rovers',
        23: 'Bristol City',
        24: 'Cardiff City',
        25: 'Coventry City',
        26: 'Huddersfield Town',
        27: 'Hull City',
        28: 'Ipswich Town',
        29: 'Leeds United',
        30: 'Leicester City',
        31: 'Middlesbrough',
        32: 'Millwall',
        33: 'Norwich City',
        34: 'Plymouth Argyle',
        35: 'Preston North End',
        36: 'Queens Park Rangers',
        37: 'Rotherham United',
        38: 'Sheffield Wednesday',
        39: 'Southampton',
        40: 'Stoke City',
    }
    teams = Team.objects.order_by('id').all()

    key = 1
    league_key = 1

    for team in teams:

        team.name = teams_mapping[key]
        team.coach_id = key
        team.league_id = league_key
        key += 1
        league_key += 1
        if key == 41:
            key = 1
        if league_key == 3:
            league_key = 1

    Team.objects.bulk_update(teams, ['name', 'coach_id', 'league_id'])

    return 'Now all teams have a name, coach and league!'


# print(give_all_clubs_a_name_coach_and_league())

def give_all_players_a_club_and_position():
    player_position_mapper = {
        1: 'GK',
        2: 'CB',
        3: 'LB',
        4: 'RB',
        5: 'LWB',
        6: 'RWB',
        7: 'CDM',
        8: 'CM',
        9: 'CAM',
        10: 'LM',
        11: 'RM',
        12: 'LW',
        13: 'RW',
        14: 'CF',
        15: 'ST'
    }
    players = FootballPlayer.objects.order_by('id').all()

    team_key = 10
    position_key = 1

    for p in players:
        p.team_id = team_key
        p.position = player_position_mapper[position_key]
        team_key += 1
        position_key += 1

        if team_key == 41:
            team_key = 1

        if position_key == 16:
            position_key = 1

    FootballPlayer.objects.bulk_update(players, ['team_id', 'position'])

    return 'Now every player has a team!'


# print(give_all_players_a_club_and_position())

def give_all_coaches_a_type():
    coach_type_mapper = {
        1: 'Head coach',
        2: 'Second coach',
    }

    coaches = FootballCoach.objects.all()

    coach_key = 1

    for coach in coaches:
        coach.type = coach_type_mapper[coach_key]
        coach_key += 1
        if coach_key == 3:
            coach_key = 1

    FootballCoach.objects.bulk_update(coaches, ['type'])

    return 'Now every coach has a type!'

# print(give_all_coaches_a_type())


# Django Queries

def get_top10_goal_scores():
    top10_players = FootballPlayer.objects.order_by('-goals', 'id')[:10]

    rank = 1
    result = []

    for player in top10_players:
        result.append(f'{rank}) {player.full_name} playing with number {player.number} '
                      f'from {player.team.name} has scored {player.goals} goals')
        rank += 1

    return_text = '\n'.join(result)
    return f'Top 10 Scorers in all leagues:\n{return_text}'

# print(get_top10_goal_scores())


def get_top10_teams_with_most_goals():
    teams = (Team.objects.prefetch_related('players')
             .annotate(goals_count=Sum('players__goals'))
             .order_by('-goals_count')[:10]
    )

    rank = 1
    result = []

    for team in teams:
        result.append(f'{rank}) Team: "{team.name}" with total of goals: {team.goals_count}')
        rank += 1

    return_text = '\n'.join(result)

    return f'Top 10 Teams with most goals:\n{return_text}'

# print(get_top10_teams_with_most_goals())


def get_league_info():
    premier_league = (League.objects.prefetch_related('teams')
               .get(id=1)
               )

    championship_league = (League.objects.prefetch_related('teams')
               .get(id=2)
               )

    def format_team_info(team):
        return f' - {team.name} FC has {team.fans} fans and plays his home matches at "{team.stadium} arena".'

    premier_league_teams = [format_team_info(team) for team in premier_league.teams.all()]
    championship_league_teams = [format_team_info(team) for team in championship_league.teams.all()]

    result_text1 = '\n'.join(premier_league_teams)
    result_text2 = '\n'.join(championship_league_teams)

    return (f'*** Premier League Teams ***\n{result_text1}'
            f'\n\n*** Championship League Teams ***\n{result_text2}')

# print(get_league_info())


def promote_coach_to_a_legend():
    all_coaches = FootballCoach.objects.all()

    for coach in all_coaches:
        if coach.years_of_experience >= 20:
            coach.type = 'Head Coach'
            coach.legendary_level = randint(8, 10)
            coach.salary = randint(1_000_000, 2_000_000)
        else:
            coach.type = coach.type
            coach.legendary_level = randint(1, 7)
            coach.salary = randint(10_000, 500_000)

    FootballCoach.objects.bulk_update(all_coaches, ['type', 'legendary_level', 'salary'])

    legendary_coaches = (FootballCoach.objects.select_related('team')
                         .filter(legendary_level__gte=8)
                         .order_by('-legendary_level', '-years_of_experience')
                         )

    legendary_coaches_list = [(f' - {c.id} {c.full_name} has Legend Level '
                               f'{c.legendary_level} stars with {c.years_of_experience} year '
                               f'of experience')for c in legendary_coaches]

    result = '\n'.join(legendary_coaches_list)
    return f'*** Legendary coaches ***\n{result}'

# print(promote_coach_to_a_legend())


def make_player_a_legend():
    promote_players = (FootballPlayer.objects
                       .filter(goals__gte=300)
                       ).update(club_legend=True, salary=F('salary') + 100_000)

    return f'{promote_players} players become a legends!'


# print(make_player_a_legend())


def remove_goalkeepers_goals():
    goalkeepers = FootballPlayer.objects.filter(position='GK')

    for gk in goalkeepers:
        if gk.id % 4 == 0:
            gk.goals = ceil(gk.id / 16)
            gk.assists = ceil(gk.id / 12)
            if gk.goals + gk.assists >= 20:
                gk.club_legend = True
        else:
            gk.goals = 0
            gk.assists = ceil(gk.id / 7)
            gk.club_legend = False

    FootballPlayer.objects.bulk_update(goalkeepers, ['goals', 'assists', 'club_legend'])

    goalkeepers_with_goal = (FootballPlayer.objects
                             .select_related('team')
                             .filter(goals__gt=0, position='GK')
                             .order_by('-goals', 'id')
                             )

    result = []
    rank = 1
    for gk in goalkeepers_with_goal:
        result.append(f'{rank}) {gk.full_name} playing for {gk.team.name} has {gk.goals} goal/s and {gk.assists} assists.')
        rank += 1

    result_text = '\n'.join(result)

    return f'*** GoalKeepers with goals ***\n{result_text}'


# print(remove_goalkeepers_goals())

