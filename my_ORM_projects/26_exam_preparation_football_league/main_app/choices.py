from django.db import models


class PositionChoices(models.TextChoices):
    GK = 'GK', 'GK'
    CB = 'CB', 'CB'
    LB = 'LB', 'LB'
    RB = 'RB', 'RB'
    LWB = 'LWB', 'LWB'
    RWB = 'RWB', 'RWB'
    CDM = 'CDM', 'CDM'
    CM = 'CM', 'CM'
    CAM = 'CAM', 'CAM'
    LM = 'LM', 'LM'
    RM = 'RM', 'RM'
    LW = 'LW', 'LW'
    RW = 'RW', 'RW'
    CF = 'CF', 'CF'
    ST = 'ST', 'ST'


class CoachTypeChoices(models.TextChoices):
    HEAD_COACH = 'Head coach', 'Head coach'
    SECOND_COACH = 'Second coach', 'Second coach'


class LeagueChoices(models.TextChoices):
    PREMIER_LEAGUE = 'Premier League', 'Premier League'
    CHAMPIONSHIP = 'Championship', 'Championship'


class TeamChoices(models.TextChoices):
    ARSENAL = 'Arsenal', 'Arsenal'
    ASTON_VILLA = 'Aston Villa', 'Aston Villa'
    BOURNEMOUTH = 'Bournemouth', 'Bournemouth'
    BRENTFORD = 'Brentford', 'Brentford'
    BRIGHTON = 'Brighton & Hove Albion', 'Brighton & Hove Albion'
    BURNLEY = 'Burnley', 'Burnley'
    CHELSEA = 'Chelsea', 'Chelsea'
    CRYSTAL_PALACE = 'Crystal Palace', 'Crystal Palace'
    EVERTON = 'Everton', 'Everton'
    FULHAM = 'Fulham', 'Fulham'
    LIVERPOOL = 'Liverpool', 'Liverpool'
    LUTON_TOWN = 'Luton Town', 'Luton Town'
    MANCHESTER_CITY = 'Manchester City', 'Manchester City'
    MANCHESTER_UNITED = 'Manchester United', 'Manchester United'
    NEWCASTLE_UNITED = 'Newcastle United', 'Newcastle United'
    NOTTINGHAM_FOREST = 'Nottingham Forest', 'Nottingham Forest'
    SHEFFIELD_UNITED = 'Sheffield United', 'Sheffield United'
    TOTTENHAM_HOTSPUR = 'Tottenham Hotspur', 'Tottenham Hotspur'
    WEST_HAM_UNITED = 'West Ham United', 'West Ham United'
    WOLVERHAMPTON_WANDERERS = 'Wolverhampton Wanderers', 'Wolverhampton Wanderers'
    BIRMINGHAM_CITY = 'Birmingham City', 'Birmingham City'
    BLACKBURN_ROVERS = 'Blackburn Rovers', 'Blackburn Rovers'
    BRISTOL_CITY = 'Bristol City', 'Bristol City'
    CARDIFF_CITY = 'Cardiff City', 'Cardiff City'
    COVENTRY_CITY = 'Coventry City', 'Coventry City'
    HUDDERSFIELD_TOWN = 'Huddersfield Town', 'Huddersfield Town'
    HULL_CITY = 'Hull City', 'Hull City'
    IPSWICH_TOWN = 'Ipswich Town', 'Ipswich Town'
    LEEDS_UNITED = 'Leeds United', 'Leeds United'
    LEICESTER_CITY = 'Leicester City', 'Leicester City'
    MIDDLESBROUGH = 'Middlesbrough', 'Middlesbrough'
    MILLWALL = 'Millwall', 'Millwall'
    NORWICH_CITY = 'Norwich City', 'Norwich City'
    PLYMOUTH_ARGYLE = 'Plymouth Argyle', 'Plymouth Argyle'
    PRESTON_NORTH_END = 'Preston North End', 'Preston North End'
    QUEENS_PARK_RANGERS = 'Queens Park Rangers', 'Queens Park Rangers'
    ROTHERHAM_UNITED = 'Rotherham United', 'Rotherham United'
    SHEFFIELD_WEDNESDAY = 'Sheffield Wednesday', 'Sheffield Wednesday'
    SOUTHAMPTON = 'Southampton', 'Southampton'
    STOKE_CITY = 'Stoke City', 'Stoke City'

    def get_team_name(cls, team_key):
        return getattr(cls, team_key, (None, None))[0]