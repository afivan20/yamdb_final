import csv
from django.core.management.base import BaseCommand
from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, User, Title, Review
from reviews.models import Genre, GenreTitle


class Command(BaseCommand):

    def handle(self, *args, **options):
        category = f'{BASE_DIR}/static/data/category.csv'
        comments = f'{BASE_DIR}/static/data/comments.csv'
        genre_title = f'{BASE_DIR}/static/data/genre_title.csv'
        genre = f'{BASE_DIR}/static/data/genre.csv'
        review = f'{BASE_DIR}/static/data/review.csv'
        titles = f'{BASE_DIR}/static/data/titles.csv'
        users = f'{BASE_DIR}/static/data/users.csv'

        Category.objects.all().delete()
        Comment.objects.all().delete()
        Title.objects.all().delete()
        Review.objects.all().delete()
        Genre.objects.all().delete()
        GenreTitle.objects.all().delete()
        User(pk=101).delete()
        User(pk=102).delete()
        User(pk=103).delete()
        User(pk=104).delete()
        User(pk=100).delete()
        reader = csv.DictReader(open(category))
        for row in reader:
            Category.objects.create(id=row['id'],
                                    name=row['name'], slug=row['slug'])

        reader = csv.DictReader(open(titles))
        for row in reader:
            Title.objects.create(id=row['id'], name=row['name'],
                                 year=row['year'], category_id=row['category'])

        reader = csv.DictReader(open(genre))
        for row in reader:
            Genre.objects.create(id=row['id'], name=row['name'],
                                 slug=row['slug'])

        user_reader = csv.DictReader(open(users))
        for row in user_reader:
            User.objects.create(id=row['id'], username=row['username'],
                                email=row['email'], role=row['role'],
                                bio=row['bio'],
                                first_name=row['first_name'],
                                last_name=row['last_name'])

        reader = csv.DictReader(open(review))
        for row in reader:

            Review.objects.create(id=row['id'], title_id=row['title_id'],
                                  text=row['text'], author_id=row['author'],
                                  pub_date=row['pub_date'], score=row['score'])

        comments = csv.DictReader(open(comments))
        for row in comments:
            Comment.objects.create(id=row['id'], review_id=row['review_id'],
                                   text=row['text'], author_id=row['author'],
                                   pub_date=row['pub_date'])

        reader = csv.DictReader(open(genre_title))
        for row in reader:
            GenreTitle.objects.create(id=row['id'], title_id=row['title_id'],
                                      genre_id=row['genre_id'])

        print('база данных обновлена , за исключением старых пользователей')
