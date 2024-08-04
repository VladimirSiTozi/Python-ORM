Django Queries Exercises:

1.	Write a Query using Django ORM to fetch all the books objects from your database.
2.	Write a Query using Django ORM to fetch title and published_date of all books from the database.
3.	Fetch first name and last name of all the new authors (Authors with popularity_score = 0 are new authors).
4.	Fetch first name and popularity score of all authors whose first name starts with (input letter) and popularity score is greater than or equal to (input popularity score), ordered by popularity_score.
5.	Fetch first name of all the authors with "ff" case insensitive in their first name, ordered by id.
6.	Fetch list of all the authors whose ids are in the list = [1, 3, 23, 43, 134, 25], ordered by id.
7.	Fetch list of all the publishers who joined after or in September 2012, output list should only contain first name and join date of publisher. Order by join date.
8.	Fetch ordered list of first 10 last names of Publishers, list must not contain duplicates.
9.	Get the sign up date for the last joined Author and Publisher.
10.	Get the first name, last name and join date of the last author who joined.
11.	Fetch list of all authors who joined after or in year 2013
12.	Fetch total price of all the books written by authors with popularity score equal to (popularity: int) or higher.
13.	Fetch list of titles of all books written by authors whose first name starts with (letter: str). The result should contain a list of the titles of every book. Not a list of tuples.
14.	Get total price of all the books written by author with pk in list (ids_list: List)
15.	Produce a list of all the authors along with their recommender.
16.	Produce list of all authors who published their book by publisher (input_id), output list should be ordered by first name.
17.	Create three new users and add in the followers of the author with pk = 1.
18.	Set the followers list of the author, with only one user with (author_input_id, user_input_id).
19.	Add new users in followers of the author with (author_input_id, user_input_id).
20.	Remove first user from the followers of the author with (author_input_id, user_input_id).
21.	Get first names of all the authors, whose user with pk = 1 is following. (Without Accessing Author.objects manager)
22.	Fetch list of all authors who wrote a book with “tle” as part of Book Title.
23.	Fetch the list of authors whose names start with ‘A’ case insensitive, and either their popularity score is greater than 5 or they have joined after 2014. with Q objects.
24.	Retrieve a specific object with primary key= 1 from the Author table.
25.	Retrieve the first N=10 records from an Author table.
26.	Retrieve records from a table that match this condition, popularity score = 7. And get the first and last record of that list.
27.	Retrieve all authors who joined after or in the year 2012, popularity score greater than or equal to 4, join date after or with date 12, and first name starts with ‘a’ (case insensitive) without using Q objects.
28.	Retrieve all authors who did not join in 2012.
29.	Retrieve Oldest author, Newest author, Average popularity score of authors, sum of price of all books in database.
30.	Retrieve all authors who have no recommender, recommended by field is null.
31.	Retrieve the books that do not have any authors, where the author is null. Also, retrieve the books whose authors are present, but do not have a recommender, where the author is not null and the author’s recommender is null. (Note that if the condition for the author not being null is not specified and only the condition for the recommender being null is mentioned, all books with both author null and author’s recommender null will be retrieved.)
32.	Total price of books written by author with primary key = 1. (Aggregation over related model), oldest book written by author with pk = 1, latest book written by author with pk=1.
33.	Among the publishers in the Publishers table what is the oldest book any publisher has published.
34.	Average price of all the books in the database.
35.	Maximum popularity score of publisher among all the publishers who published a book for the author with pk = 1. (Reverse Foreign Key hop)
36.	Count the number of authors who have written a book which contains the phrase ‘ab’ case insensitive.
37.	Get all the authors with followers more than 216.
38.	Get average popularity score of all the authors who joined after 20 September 2014.
39.	Generate a list of books whose author has written more than 10 books.
40.	Get the list of books with duplicate titles.
