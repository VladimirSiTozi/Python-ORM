import os
from random import randint
from typing import List

import django
import random

from django.db.models import Sum
from django.template.defaultfilters import upper

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from populate_db import populate_authors, populate_publishers, populate_books, populate_users
from main_app.models import Author, Publisher, Book, User


# Create queries within functions

def create_authors_publishers_book_users():
    print(populate_authors())
    print(populate_publishers())
    print(populate_books())
    print(populate_users())
    print('authors, publishers, books, users are created!')


def populate_left_data():
    for a in Author.objects.all():
        a.recommendedby_id = randint(1, 200)
        a.save()

    print('done!')

    for a in Publisher.objects.all():
        a.recommendedby_id = randint(1, 100)
        a.save()

    print('done!')

    follower_ids = list(User.objects.values_list('id', flat=True))

    for author in Author.objects.all():
        # Ensure not to include the author's own ID in the followers
        available_user_ids = [uid for uid in follower_ids if uid != author.id]

        # Sample 10 unique user IDs
        followers_to_add = random.sample(available_user_ids, min(10, len(available_user_ids)))

        # Retrieve the User objects for the selected IDs
        followers = User.objects.filter(id__in=followers_to_add)

        # Add the selected followers to the current author
        author.followers.add(*followers)

    print('done!')
    print('all models data is populate!')


# 1.
def all_books():
    books = Book.objects.all()

    return books

# print(all_books())


# 2.
def all_book_titles_and_published_date():
    books = Book.objects.values_list('title', 'published_date').all()

    return books

# print(all_book_titles_and_published_date())


# 3.
def new_authors():
    authors = Author.objects.values('first_name', 'last_name').filter(popularity_score=0)

    result_list = []
    for a in authors:
        result_list.append(f' - {a["first_name"]} {a["last_name"]}')

    text = '\n'.join(result_list)

    return f"*** NEW AUTHORS ***\n{text}"

# print(new_authors())


# 4.
def authors_first_name_and_popularity(letter: str, popularity: int):
    authors = (Author.objects.values('first_name', 'popularity_score')
               .filter(popularity_score__gte=popularity, first_name__startswith=upper(letter))
               .order_by('-popularity_score')
               )

    result_list = []
    for a in authors:
        result_list.append(f' - {a["first_name"]} with popularity {a["popularity_score"]}')

    text = '\n'.join(result_list)

    return f"*** AUTHORS - First name starts with '{upper(letter)}' and popularity greater than {popularity - 1} ***\n{text}"

# print(authors_first_name_and_popularity('a', 8))


# 5.
def author_first_name_contains_aa():
    authors = Author.objects.values('first_name').filter(first_name__icontains='ff').order_by('id')

    result_list = []
    for a in authors:
        result_list.append(f' - {a["first_name"]} ')

    text = '\n'.join(result_list)

    return f"*** AUTHORS - Contains 'ff' in first_name ***\n{text}"

# print(author_first_name_contains_aa())


# 6.
def authors_with_exact_id():
    authors = Author.objects.filter(id__in=[1, 3, 23, 43, 134, 25]).order_by('id')

    result_list = []
    for a in authors:
        result_list.append(f'{a.first_name} {a.last_name} with id #{a.id}')

    return f"*** AUTHORS - With id in [1, 3, 23, 43, 134, 25] ***\n{result_list}"

# print(authors_with_exact_id())


# 7.
def authors_joined_after_september_2012():
    authors = Author.objects.filter(join_date__gte='2012-09-01').order_by('join_date')

    result_list = []
    for a in authors:
        result_list.append(f'#{a.id} {a} joined at {a.join_date}')

    return f"*** AUTHORS - Joined after September 2012 ***\n{result_list}"

# print(authors_joined_after_september_2012())


# 8.
def first_10_publishers():
    publishers = Publisher.objects.values('last_name', 'join_date').distinct('last_name').order_by('last_name')[:10]

    print(f"*** Publishers - First 10, only last names without duplicates ***")

    return publishers

# print(first_10_publishers())


# 9. ***
# model._meta.object_name == "Author" or "Publisher"
def last_joined_author_and_publisher():
    last_publisher = Publisher.objects.order_by('-join_date').first()
    last_author = Author.objects.order_by('-join_date').first()

    result = []

    for person in [last_author, last_publisher]:
        result.append(f' - {person} with id #{person.id} is the last joined '
                      f'{"author" if person._meta.object_name == "Author" else "publisher"} at {person.join_date}')

    text = '\n'.join(result)

    return f"*** Author & Publishers - Last joined author and publisher ***\n{text}"

# print(last_joined_author_and_publisher())


# 10.
def last_joined_author():
    last_author = Author.objects.order_by('-join_date').first()

    text = f' - {last_author} is the last joined author, joined at {last_author.join_date}'

    return f"*** Author - Last joined author ***\n{text}"

# print(last_joined_author())


# 11.
def authors_joined_in_or_after_2013():
    authors = Author.objects.filter(join_date__gte='2013-01-01')

    print('*** Author - Joined after or in year 2013 ***')

    return authors

# print(authors_joined_in_or_after_2013())


# 12.
def total_price_of_all_books_by_authors_with_popularity_over(popularity: int):
    books = (Book.objects.select_related('author')
             .filter(author__popularity_score__gte=popularity)
             .aggregate(total_price=Sum('price'))
             )

    return (f'*** Total price of all books with authors with popularity equal or higher of {popularity} is: ***'
            f'\n - {books["total_price"]:.2f}$')

# print(total_price_of_all_books_by_authors_with_popularity_over(7))


# 13.
def all_books_with_authors_starts_with(letter: str):
    books = (Book.objects.select_related('author')
             .filter(author__first_name__istartswith=letter)
             .values_list('title', flat=True)
             )

    print(f'*** Book - Titles written by authors starting with "{letter}" ***')

    return books

# print(all_books_with_authors_starts_with('A'))
# print(all_books_with_authors_starts_with('b'))
# print(all_books_with_authors_starts_with('c'))


# 14.
def total_price_of_all_books_by_authors_with_id(ids_list: List):
    books = (Book.objects.select_related('author')
             .filter(author_id__in=ids_list)
             .aggregate(total_price=Sum('price'))
             )

    return (f'*** Total price of all books with authors with ids in {ids_list} is: ***'
            f'\n - {books["total_price"]:.2f}$')

# print(total_price_of_all_books_by_authors_with_id([1, 2, 3]))
# print(total_price_of_all_books_by_authors_with_id([101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]))
# print(total_price_of_all_books_by_authors_with_id([50, 60]))


# 15.
def all_authors_and_their_recommender():
    authors = Author.objects.all().values('first_name', 'last_name', 'recommendedby__first_name', 'recommendedby__last_name')

    print(f'*** Author - authors and their recommenders" ***')

    return authors

# print(all_authors_and_their_recommender())


# 16.
def all_authors_with_publisher_id(input_id):
    authors = (Author.objects.prefetch_related('books')
               .filter(books__publisher_id=input_id)
               .order_by('first_name')
               .distinct()
               )

    result = []

    for author in authors:
        result.append(f' - {author} with id #{author.id}')

    text = '\n'.join(result)

    return f'*** Authors - Published their with publisher id #{input_id} ***\n{text}'

# print(all_authors_with_publisher_id(1))


# 17.
def create_three_users():
    user1 = User.objects.create(
        username='user1',
        email='user1@test.com'
    )

    user2 = User.objects.create(
        username='user2',
        email='user2@test.com'
    )

    user3 = User.objects.create(
        username='user3',
        email='user3@test.com'
    )

    author = Author.objects.get(id=1)

    author.followers.add(user1, user2, user3)

    return f'*** Notification ***\n3 new users followed {author}'

# print(create_three_users())


# 18.
def set_followers_to_author(author_input_id, user_input_id):
    user = User.objects.get(id=user_input_id)
    author = Author.objects.get(id=author_input_id)

    author.followers.set([user])

    return f'*** Notification ***\n{author} has first follower - {user}'

# print(set_followers_to_author(2, 1003))


# 19.
def add_new_user_to_author_followers(author_input_id, user_input_id):
    author = Author.objects.get(id=author_input_id)
    user = User.objects.get(id=user_input_id)

    author.followers.add(user)

    return f'*** Notification ***\n - {user} has followed book author {author}'

print(add_new_user_to_author_followers(1, 505))


# 20.
def remove_first_follower_from_author_followers(author_input_id):
    author = Author.objects.prefetch_related('followers').get(id=author_input_id)
    user = author.followers.order_by('id').first()

    author.followers.remove(user)

    return f'*** Notification ***\n- {user} unfollowed - {author}'

# print(remove_first_follower_from_author_followers(1))







