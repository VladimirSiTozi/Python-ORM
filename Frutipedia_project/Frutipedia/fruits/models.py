from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(2),
            RegexValidator(regex='^[a-zA-Z]+$', message='Fruit name should contain only letters!')
        ]
    )

    image_url = models.URLField(
        null=False,
        blank=False
    )

    description = models.TextField(
        null=False,
        blank=False
    )

    nutrition = models.TextField(
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        null=True
    )
