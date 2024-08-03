from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from main_app.models_custom_managers import AstronautManager
from main_app.models_mixins import UpdatedAtMixin, LaunchDateMixin, NameMixin


# Create your models here.

class Astronaut(NameMixin, UpdatedAtMixin):
    # name = models.CharField(
    #     max_length=120,
    #     validators=[
    #         MinLengthValidator(2)
    #     ]
    # )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\d+$')
        ]
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    # updated_at = models.DateField(
    #     auto_now=True
    # )

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    # name = models.CharField(
    #     max_length=120,
    #     validators=[
    #         MinLengthValidator(2)
    #     ]
    # )

    manufacturer = models.CharField(
        max_length=100
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )

    # launch_date = models.DateField()
    #
    # updated_at = models.DateField(
    #     auto_now=True
    # )


class Mission(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    # name = models.CharField(
    #     max_length=120,
    #     validators=[
    #         MinLengthValidator(2)
    #     ]
    # )

    description = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default='Planned'
    )

    # launch_date = models.DateField()
    #
    # updated_at = models.DateField(
    #     auto_now=True
    # )

    spacecraft = models.ForeignKey(
        Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions'
    )

    astronauts = models.ManyToManyField(
        Astronaut,
        related_name='missions'
    )

    commander = models.ForeignKey(
        Astronaut,
        on_delete=models.SET_NULL,
        related_name='commanded_missions',
        blank=True,
        null=True
    )
