from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.

class BasePerson(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, 'First name must be at least 2 symbols')
        ]
    )

    last_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, 'Last name must be at least 2 symbols')
        ]
    )

    join_date = models.DateField()

    popularity_score = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Author(BasePerson):
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    zipcode = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    telephone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    recommendedby = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='recommended_authors',
        related_query_name='recommended_authors',
        null=True,
        blank=True
    )

    followers = models.ManyToManyField(
        'User',
        related_name='followed_authors',
        related_query_name='followed_authors'
    )


class Publisher(BasePerson):
    recommendedby = models.ForeignKey(
        'Publisher',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Book(models.Model):
    class GenreChoices(models.TextChoices):
        FICTION = 'F', 'Fiction'
        BIOGRAPHY = 'B', 'Biography'
        SCIENCE_FICTION = 'SF', 'Science Fiction'
        FANTASY = 'FA', 'Fantasy'
        MYSTERY = 'MY', 'Mystery'
        THRILLER = 'TH', 'Thriller'
        ROMANCE = 'RO', 'Romance'
        HORROR = 'HO', 'Horror'
        CRIMINAL = 'C', 'Criminal'
        CHILDREN_LITERATURE = 'CL', "Children's literature"

    title = models.CharField(
        max_length=250
    )

    genre = models.CharField(
        max_length=50,
        choices=GenreChoices.choices
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    published_date =models.DateField()

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        related_query_name='books'
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        related_query_name='books'
    )

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, 'First name must be at least 2 symbols')
        ]
    )

    email = models.EmailField()

    def __str__(self):
        return self.username

