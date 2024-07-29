from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

from main_app.choices import PositionChoices, CoachTypeChoices, LeagueChoices, TeamChoices


# Create your models here.

class BasePerson(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5, message='Full name must be at least 5 symbols')
        ]
    )

    birth_date = models.DateField()

    nationality = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message='Nationality must be at least 2 symbols long')
        ]
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.full_name


class FootballPlayer(BasePerson):
    position = models.CharField(
        max_length=3,
        choices=PositionChoices.choices,
        blank=True,
        null=True
    )

    number = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99),
            MinValueValidator(0)
        ]
    )

    goals = models.PositiveIntegerField()

    assists = models.PositiveIntegerField()

    club_legend = models.BooleanField()

    # should be in class BasePerson as a /team/
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='players',
        blank=True,
        null=True
    )


class FootballCoach(BasePerson):
    years_of_experience = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(30)
        ]
    )

    type = models.CharField(
        max_length=15,
        choices=CoachTypeChoices.choices,
        blank=True,
        null=True
    )

    legendary_level = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )


class League(models.Model):
    name = models.CharField(
        max_length=50,
        choices=LeagueChoices.choices,
        blank=True,
        null=True
    )

    prize_money = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    start_date = models.DateField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(
        max_length=50,
        choices=TeamChoices.choices,
        blank=True,
        null=True
    )

    fans = models.PositiveIntegerField()

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stadium = models.CharField(
        max_length=50
    )

    # should be in class BasePerson as a /team/
    coach = models.OneToOneField(
        FootballCoach,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='teams',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
