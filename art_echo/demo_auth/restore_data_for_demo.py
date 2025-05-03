import os

from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import management
from django.core.files import File

User = get_user_model()
NALIVKIN_USERNAME = config('NALIVKIN_USERNAME')

fixtures_dir = os.path.join(settings.BASE_DIR, 'demo_auth', 'fixtures')


def reset_demo_data():
    """
    Полностью сбрасывает и восстанавливает демонстрационные данные
    в базе данных.

    Назначение:
    -----------
    Используется для восстановления заранее подготовленного состояния
    базы данных для демонстрационного пользователя (например, "Наливкин").
    Полезно при показе возможностей проекта без риска повредить
    реальные данные.

    Механизм работы:
    ----------------
    1. Загружает фикстуры (json-файлы) в определённые таблицы
       базы данных с помощью кастомной команды `reset_bd_from_fixtures`
       из приложения `custom_commands`.

    2. Удаляет лишние записи с флагом `is_demo=True` и id выше
       допустимого порога с помощью других кастомных команд
       (`delete_records_with_conditions` и
       `delete_records_with_conditions_by_model`).

    3. Удаляет текущий аватар пользователя-демо (если установлен)
       и копирует оригинальный аватар из файла, указанного
       в `settings.DEMO_USER_ORIGINAL_AVATAR`.

    Команды, выполняемые в рамках сброса, перечислены в виде
    кортежей и охватывают все ключевые модели: пользователей,
    категории, жанры, тайтлы, рецензии, комментарии
    и промежуточные связи.

    Зависимости:
    ------------
    - Кастомные команды из приложения `custom_commands`:
        - `reset_bd_from_fixtures`
        - `delete_records_with_conditions`
        - `delete_records_with_conditions_by_model`
    - Файл аватара: `settings.DEMO_USER_ORIGINAL_AVATAR`
    - Статический username демо-пользователя: `NALIVKIN_USERNAME`

    Примечание:
    -----------
    Функция должна вызываться только в безопасной среде,
    предназначенной для демонстраций, так как она перезаписывает
    и удаляет данные в базе.
    """

    commands = (
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'user.json'), 'users_user'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'confirmation_code.json'),
            'users_confirmationcode'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'category.json'), 'reviews_category'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'genre.json'), 'reviews_genre'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'title.json'), 'reviews_title'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'review.json'), 'reviews_review'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'comment.json'), 'reviews_comment'
        ),
        (
            'reset_bd_from_fixtures',
            os.path.join(fixtures_dir, 'reviews_title_genre.json'),
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
        demo_user.avatar.delete(save=False)

    # Копируем оригинальный аватар из указанного пути
    if os.path.exists(settings.DEMO_USER_ORIGINAL_AVATAR):
        with open(settings.DEMO_USER_ORIGINAL_AVATAR, 'rb') as f:
            demo_user.avatar.save(
                os.path.basename(settings.DEMO_USER_ORIGINAL_AVATAR),
                File(f),
                save=True
            )

    for cmd in commands:
        management.call_command(cmd[0], *cmd[1:])
