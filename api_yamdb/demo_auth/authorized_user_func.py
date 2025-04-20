import os

from decouple import config
# from django.apps import apps
# from django.conf import settings
# from django.contrib.auth.models import User
from django.core import serializers
from django.core.management import call_command

# NALIVKIN_USERNAME = config('NALIVKIN_USERNAME')

fixtures_commands = (
    'python manage.py dumpdata --indent=2 users.User -o demo_auth/fixtures/user.json',
    'python manage.py dumpdata --indent=2 users.ConfirmationCode -o demo_auth/fixtures/confirmation_code.json',
    'python manage.py dumpdata --indent=2 reviews.Category -o demo_auth/fixtures/category.json',
    'python manage.py dumpdata --indent=2 reviews.Genre -o demo_auth/fixtures/genre.json',
    'python manage.py dumpdata --indent=2 reviews.Title -o demo_auth/fixtures/title.json',
    'python manage.py dumpdata --indent=2 reviews.Title.genres.through -o demo_auth/fixtures/reviews_title_genre.json',
    'python manage.py dumpdata --indent=2 reviews.Review -o demo_auth/fixtures/review.json',
    'python manage.py dumpdata --indent=2 reviews.Comment -o demo_auth/fixtures/comment.json',

)

fixtures_commands = (
    ('dumpdata', 'users.User', '--indent=2', '-o', 'demo_auth/fixtures/user.json'),
    ('dumpdata', 'users.ConfirmationCode', '--indent=2', '-o', 'demo_auth/fixtures/confirmation_code.json'),
    ('dumpdata', 'reviews.Category', '--indent=2', '-o', 'demo_auth/fixtures/category.json'),
    ('dumpdata', 'reviews.Genre', '--indent=2', '-o', 'demo_auth/fixtures/genre.json'),
    ('dumpdata', 'reviews.Title', '--indent=2', '-o', 'demo_auth/fixtures/title.json'),
    ('dumpdata', 'reviews.Title.genres.through', '--indent=2', '-o', 'demo_auth/fixtures/reviews_title_genre.json'),
    ('dumpdata', 'reviews.Review', '--indent=2', '-o', 'demo_auth/fixtures/review.json'),
    ('dumpdata', 'reviews.Comment', '--indent=2', '-o', 'demo_auth/fixtures/comment.json'),
)

for command in fixtures_commands:
    call_command(*command)

# def restore_user_data():
#     catygory_model = apps.get_model('reviews', 'Category')
#     gerne_model = apps.get_model('reviews', 'Genre')
#     title_model = apps.get_model('reviews', 'Title')
#     review_model = apps.get_model('reviews', 'Review')
#     comment_model = apps.get_model('reviews', 'Comment')
#     user_model = apps.get_model('users', 'User')
#     confirmation_code_model = apps.get_model('users', 'ConfirmationCode')

#     posts_file_path = os.path.join(
#         settings.BASE_DIR,
#         'core/authorized_user_fixtures/backup_posts.json')
#     comments_file_path = os.path.join(
#         settings.BASE_DIR,
#         'core/authorized_user_fixtures/backup_comments.json')
#     groups_file_path = os.path.join(
#         settings.BASE_DIR,
#         'core/authorized_user_fixtures/backup_groups.json')

#     with open(posts_file_path, 'r') as posts_file:
#         posts_json = posts_file.read()

#     with open(comments_file_path, 'r') as comments_file:
#         comments_json = comments_file.read()

#     with open(groups_file_path, 'r') as groups_file:
#         groups_json = groups_file.read()

#     posts = list(serializers.deserialize('json', posts_json))
#     comments = list(serializers.deserialize('json', comments_json))
#     groups = list(serializers.deserialize('json', groups_json))
#     user = User.objects.get(username=NALIVKIN_USERNAME)

#     all_posts = post_model.objects.filter(author=user)
#     all_comments = comment_model.objects.filter(author=user)
#     all_groups = group_model.objects.filter(creator=user)

#     posts_to_delete = all_posts.exclude(
#         id__in=[post.object.pk for post in posts])
#     comments_to_delete = all_comments.exclude(
#         id__in=[comment.object.pk for comment in comments])
#     groups_to_delete = all_groups.exclude(
#         id__in=[group.object.pk for group in groups])

#     posts_to_delete.delete()
#     comments_to_delete.delete()
#     groups_to_delete.delete()
