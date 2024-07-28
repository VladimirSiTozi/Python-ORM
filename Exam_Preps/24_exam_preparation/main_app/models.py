from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

from main_app.custom_managers import AuthorManager


# Create your models here.


class ContentMixin(models.Model):
    class Meta:
        abstract = True

    content = models.TextField(
        validators=[
            MinLengthValidator(10)
        ]
    )


class PublishedOnMixin(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )

    email = models.EmailField(
        unique=True
    )

    is_banned = models.BooleanField(
        default=False
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ]
    )

    website = models.URLField(
        null=True,
        blank=True
    )

    objects = AuthorManager()

    def __str__(self):
        return self.full_name


class Article(ContentMixin, PublishedOnMixin):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ]
    )

    category = models.CharField(
        choices=CategoryChoices.choices,
        max_length=10,
        default='Technology'
    )

    authors = models.ManyToManyField(
        Author,
    )

    def __str__(self):
        return self.title


class Review(ContentMixin, PublishedOnMixin):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='author_reviews'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_reviews'
    )