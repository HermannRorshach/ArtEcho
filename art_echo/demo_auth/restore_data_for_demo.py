import os

from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import management
from django.core.files import File

User = get_user_model()
NALIVKIN_USERNAME = config('NALIVKIN_USERNAME')


def reset_demo_data():
    commands = (
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/user.json', 'users_user'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/confirmation_code.json',
            'users_confirmationcode'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/category.json', 'reviews_category'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/genre.json', 'reviews_genre'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/title.json', 'reviews_title'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/review.json', 'reviews_review'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/comment.json', 'reviews_comment'
        ),
        (
            'reset_bd_from_fixtures',
            'demo_auth/fixtures/reviews_title_genre.json',
            'reviews_title_genre'
        ),

        (
            'delete_records_with_conditions',
            'users_user', 'is_demo=True AND id > 109', '-r'
        ),
        (
            'delete_records_with_conditions',
            'users_confirmationcode', 'is_demo=True', '-r'
        ),
        (
            'delete_records_with_conditions',
            'reviews_category', 'is_demo=True AND id > 6', '-r'
        ),
        (
            'delete_records_with_conditions',
            'reviews_genre', 'is_demo=True AND id > 30', '-r'
        ),
        (
            'delete_records_with_conditions_by_model',
            'reviews.Title', 'is_demo=True, pk__gt=64'
        ),
        (
            'delete_records_with_conditions',
            'reviews_review', 'is_demo=True AND id > 147', '-r'
        ),
        (
            'delete_records_with_conditions',
            'reviews_comment', 'is_demo=True AND id > 19', '-r'
        ),
    )

    demo_user = User.objects.get(username=NALIVKIN_USERNAME)

    # Удаляем текущий аватар, если он есть
    if demo_user.avatar:
        print('удаляем аватар')
        demo_user.avatar.delete(save=False)

    # Копируем оригинальный аватар из указанного пути
    if os.path.exists(settings.DEMO_USER_ORIGINAL_AVATAR):
        print('Директория доступна')
        with open(settings.DEMO_USER_ORIGINAL_AVATAR, 'rb') as f:
            demo_user.avatar.save(
                os.path.basename(settings.DEMO_USER_ORIGINAL_AVATAR),
                File(f),
                save=True
            )

    for cmd in commands:
        management.call_command(cmd[0], *cmd[1:])
