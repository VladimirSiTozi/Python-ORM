import datetime
import os
from random import randint
from typing import List

import django
import random

from django.db.models import Sum, Q, Min, Max, Avg, Count
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

# print(add_new_user_to_author_followers(1, 505))


# 20.
def remove_first_follower_from_author_followers(author_input_id):
    author = Author.objects.prefetch_related('followers').get(id=author_input_id)
    user = author.followers.order_by('id').first()

    author.followers.remove(user)

    return f'*** Notification ***\n- {user} unfollowed - {author}'

# print(remove_first_follower_from_author_followers(1))


# 21.
def select_authors_through_users():
    authors = User.objects.get(id=1).followed_authors.all().values('first_name')

    print(f'*** Authors - Through Users ***')

    return authors

# print(select_authors_through_users())


# 22.
def authors_and_their_books_containing(input_text: str):
    authors = Author.objects.prefetch_related('books').filter(books__title__icontains=input_text)

    print(f'*** Authors - Who wrote book with "{input_text}" as part of Book Title ***')

    return authors

# print(authors_and_their_books_containing('Bed of'))


# 23.
def author_complex_query(input_letter: str):
    query = (Q(first_name__istartswith=input_letter) & Q(last_name__istartswith=input_letter) &
             Q(Q(popularity_score__gt=30) | Q(join_date__gt='2014-01-01')))
    author = Author.objects.filter(query)

    print(f'*** Authors - whose names start with ‘{input_letter}’ case insensitive, and either their popularity score '
          f'is greater than 30 or they have joined after 2014 ***')

    return author

# print(author_complex_query('b'))
# print(author_complex_query('m'))
# print(author_complex_query('t'))


# 24.
def retrieve_specific_object():
    author = Author.objects.get(id=1)

    print(f'*** Authors - Retrieve a specific object with primary key= 1 ***')

    return author

# print(retrieve_specific_object())


# 25.
def retrieve_first_10_authors():
    authors = Author.objects.all()[:10]

    result = []

    for author in authors:
        result.append(f' - {author}')

    text = '\n'.join(result)

    return f'*** Authors - First 10 authors ***\n{text}'

# print(retrieve_first_10_authors())


# 26.
def retrieve_first_and_last_author_with_popularity(input_popularity: int):
    author = Author.objects.filter(popularity_score=input_popularity)

    author1 = author.first()
    author2 = author.last()

    result = [f' - First is {author1}',
              f' - Last is {author2}']

    text = '\n'.join(result)

    return f'*** Authors - First and Last authors with popularity equal to {input_popularity} ***\n{text}'

# print(retrieve_first_and_last_author_with_popularity(99))


# 27.
def author_complex_query2(join_year: int, popularity: int, join_day: int, letter: str):
    author = Author.objects.filter(join_date__year__gte=join_year,
                                   popularity_score__gte=popularity,
                                   join_date__day__gte=join_day,
                                   first_name__istartswith=letter)

    return (f'*** Authors - Who joined after or in the year {join_year}, popularity score greater than or equal to '
            f'{popularity}, after or with date {join_day}, and first name starts with "{letter}" (case insensitive) ***'
            f'\n {author}')

# print(author_complex_query2(2012, 40, 12, 'a'))


# 28.
def authors_did_not_join_in_year(year: int):
    query = ~Q(join_date__year=str(year))
    author = Author.objects.filter(query)

    print(f"*** Authors - Who didn't join in {year} ***")

    return author

# print(authors_did_not_join_in_year(2012))


# 29.
def avg_popularity_score_and_sum_of_price():
    oldest_author = Author.objects.aggregate(Min('join_date'))
    # oldest_author = Author.objects.order_by('join_date').first()

    newest_author = Author.objects.aggregate(Max('join_date'))
    # newest_author = Author.objects.order_by('join_date').last()

    avg_popularity = Author.objects.aggregate(Avg('popularity_score'))

    total_price = Book.objects.aggregate(Sum('price'))

    return [oldest_author, newest_author, avg_popularity, total_price]

# print(avg_popularity_score_and_sum_of_price())


# 30.
def authors_without_recommender():
    author = Author.objects.filter(recommended_authors__isnull=True)

    print(f"*** Authors - Without recommender ***")

    return author

# print(authors_without_recommender())


# 31.
def books_complex_query():
    books1 = Book.objects.filter(author__isnull=True)
    books2 = Book.objects.filter(author__isnull=True, author__recommendedby__isnull=True)

    print(f"*** Books - Without author and author has no recommender ***")

    return [books1, books2]

# print(books_complex_query())


# 32.
def multiple_queries(input_id):
    total_price = Book.objects.filter(author_id=input_id).aggregate(Sum('price'))

    oldest_book = Book.objects.filter(author_id=input_id).order_by('published_date').first()

    newest_book = Book.objects.filter(author_id=input_id).order_by('published_date').last()

    print(f"*** Books - Total price of books, oldest and newest book by author with id # {input_id} ***")

    return [total_price, oldest_book, newest_book]

# print(multiple_queries(1))


# 33.
def oldest_published_book_for_every_publisher():
    publishers = Publisher.objects.prefetch_related('books')

    result = []

    for publisher in publishers:
        result.append(f' - {publisher} {publisher.books.order_by("published_date").first()}')

    text = '\n'.join(result)

    return f'*** Publisher - and their oldest published books ***\n{text}'

# print(oldest_published_book_for_every_publisher())


# 34.
def avg_price_of_all_books():
    price = Book.objects.aggregate(avg_price=Avg('price'))

    return f'*** Books - Average price of all books ***\n - {price["avg_price"]:.2f}$ '

# print(avg_price_of_all_books())


# 35.
def max_popularity_of_publishers(input_author_id: int):
    max_popularity = (Publisher.objects.prefetch_related('books')
                      .filter(books__author_id=input_author_id)
                      .aggregate(max_ps=Max('popularity_score'))
                      )

    return (f'*** Publisher - with max popularity who published a book with author id #{input_author_id} '
            f'is with {max_popularity["max_ps"]} popularity score ***')

# print(max_popularity_of_publishers(2))
# print(max_popularity_of_publishers(3))
# print(max_popularity_of_publishers(199))


# 36.
def authors_count_written_a_book_containing(input_text: str):
    authors_count = (Author.objects.filter(books__title__icontains=input_text)
                     .aggregate(au_count=Count('id'))
                     )

    return (f'*** Authors - who have written a book which contains the phrase ‘{input_text}’ case insensitive ***'
            f'\n - Their count is {authors_count["au_count"]}.')

# print(authors_count_written_a_book_containing('ab'))


# 37.
def authors_with_followers_more_than(followers_number: int):
    authors = Author.objects.annotate(f_count=Count('followers')).filter(f_count__gt= followers_number)

    print(f'*** Authors - who have followers more than {followers_number} ***')

    return authors

# print(authors_with_followers_more_than(10))


# 38.
def avg_popularity_of_authors_after_2014():
    authors = Author.objects.filter(join_date__gt='2014-09-20').aggregate(avg_ps=Avg('popularity_score'))
    # authors = (Author.objects.filter(join_date__gt=datetime.date(year=2014, month=9, day=20))
    #            .aggregate(avg_ps=Avg('popularity_score')))

    print(f'*** Authors - average popularity who joined after 20 September 2014 ***')

    return f' - avg_popularity = {authors["avg_ps"]:.2f}'

# print(avg_popularity_of_authors_after_2014())


# 39.
def books_by_author_with_more_than_10_books():
    books = (Book.objects.annotate(b_count=Count('author__books'))
             .filter(b_count__gt=10)
             .distinct()
             )

    print(f'*** Books - list of books whose author has written more than 10 books ***')

    return books

# print(books_by_author_with_more_than_10_books())


# 40.
def duplicate_titles():
    books = Book.objects.annotate(count_title=Count('title')).filter(count_title__gt=1)

    return books

# print(duplicate_titles())
