import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Actor, Director, Movie
from django.db.models import Q, Count, Avg, F


# from populate_db import populate_model_with_data

# Create queries within functions
# populate_model_with_data(Director, 5)
# populate_model_with_data(Actor, 10)
# populate_model_with_data(Movie, 20)

# print(Director.objects.get_directors_by_movies_count())


def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)

    elif search_name is not None:
        query = query_name

    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []

    for d in directors:
        result.append(f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}')

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if top_director:
        return f'Top Director: {top_director.full_name}, movies: {top_director.movies_count}.'
    return ''


def get_top_actor():
    top_actor = (Actor.objects.prefetch_related('starring_movies')
                 .annotate(movies_count=Count('starring_movies'),
                           avg_rating=Avg('starring_movies__rating'))
                 ).order_by('-movies_count', 'full_name').first()

    if not top_actor or not top_actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all() if m)

    return (f"Top Actor: {top_actor.full_name}, starring in movies: {movies},"
            f", movies average rating: {top_actor.avg_rating:.1f}")

# print(get_directors(search_name='S', search_nationality=None))
# print(get_top_director())


def get_actors_by_movies_count():
    actors = (Actor.objects.prefetch_related('actor_movies')
              .annotate(movies_count=Count('actor_movies'))
              ).order_by('-movies_count', 'full_name')[:3]

    result = []

    for a in actors:
        result.append(f'{a.full_name}, participated in {a.movies_count} movies')

    return '\n'.join(result)

# print(get_actors_by_movies_count())


def get_top_rated_awarded_movie():
    movie = (Movie.objects.select_related('starring_actor')
             .prefetch_related('actors')
             .filter(is_awarded=True)
             .order_by('-rating', 'title')
             ).first()

    if movie is None:
        return ''

    starring_actor = movie.starring_actor.full_name
    if starring_actor is None:
        starring_actor = 'N/A'

    actors = movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ', '.join(actors)

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: "
            f"{starring_actor}. Cast: {cast}.")


print(get_top_rated_awarded_movie())


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10).all()

    if not movies:
        return "No ratings increased."

    movies_count = movies.count()

    movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {movies_count} movies."
