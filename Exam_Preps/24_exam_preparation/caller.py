import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


# Create queries within functions

# print(Author.objects.get_authors_by_article_count())

def get_authors(search_name=None, search_email=None) -> str:
    if search_email is None and search_name is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = Q(query_name & query_email)

    elif search_name is not None:
        query = query_name

    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    result = [f'Author: {a.full_name}, email: {a.email}, status: {"Banned" if a.is_banned else "Not Banned"}' for a in authors]

    return '\n'.join(result)


# print(get_authors('Ivan Ivanov', None))


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if not top_author:
        return ''

    return f'Top Author: {top_author.full_name} with {top_author.article_count} published articles.'


# print(get_top_publisher())

def get_top_reviewer():
    top_reviewer = (Author.objects.annotate(review_count=Count('author_reviews'))
                    .order_by('-review_count', 'email')
                    .first()
                    )

    if not top_reviewer:
        return ''

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews.'


# print(get_top_reviewer())

def get_latest_article():
    # try:
    latest_article = (Article.objects.prefetch_related('authors', 'article_reviews')
                      .annotate(article_count=Count('id'), avg_rating=Avg('article_reviews__rating'))
                      .order_by('-published_on')
                      .first()
                      )

    if not latest_article:
        return ''

    authors = latest_article.authors.order_by('full_name').all()
    result_authors = [a.full_name for a in authors]

    return (f'The latest article is: {latest_article.title}. '
            f'Authors: {", ".join(result_authors)}. '
            f'Reviewed: {latest_article.article_count:.0f} times. Average Rating: {latest_article.avg_rating:.2f}.')

    # except Exception as e:
    #     return ''

# print(get_latest_article())


def get_top_rated_article():
    top_article = (Article.objects.prefetch_related('article_reviews')
                   .annotate(avg_rating=Avg('article_reviews__rating'), reviews_count=Count('article_reviews'))
                   .order_by('-avg_rating', 'title')
                   .first()
                   )

    if not top_article:
        return ''

    return (f'The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, '
            f'reviewed {top_article.reviews_count} times.')

# print(get_top_rated_article())


def ban_author(email=None):

    author = Author.objects.prefetch_related('author_reviews').filter(email=email).first()

    if not author:
        return "No authors banned."

    deleted_reviews_count = Review.objects.filter(author=author).delete()

    author.is_banned = True
    author.save()

    return f'Author: {author.full_name} is banned! {deleted_reviews_count[0]} reviews deleted.'


# print(ban_author('ivan@ivan.com'))

