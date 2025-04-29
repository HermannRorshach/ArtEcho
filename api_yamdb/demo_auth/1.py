import subprocess
import os
import sys

# Принудительно устанавливаем UTF-8 для всей системы
os.environ['PYTHONUTF8'] = '1'
if sys.platform == 'win32':
    # Для Windows 10+ можно принудительно установить UTF-8 в консоли
    subprocess.run('chcp 65001', shell=True, check=True)
    os.environ['PYTHONIOENCODING'] = 'utf-8'

fixtures_commands = [
    'python manage.py dumpdata --indent=2 users.User -o demo_auth/fixtures/user.json',
    # 'python manage.py dumpdata --indent=2 users.ConfirmationCode -o demo_auth/fixtures/confirmation_code.json',
    # 'python manage.py dumpdata --indent=2 reviews.Category -o demo_auth/fixtures/category.json',
    # 'python manage.py dumpdata --indent=2 reviews.Genre -o demo_auth/fixtures/genre.json',
    # 'python manage.py dumpdata --indent=2 reviews.Title -o demo_auth/fixtures/title.json',
    # 'python manage.py dumpdata --indent=2 reviews.Review -o demo_auth/fixtures/review.json',
    # 'python manage.py dumpdata --indent=2 reviews.Comment -o demo_auth/fixtures/comment.json',
    # 'python manage.py dumpdata --indent=2 reviews.Title_genre -o demo_auth/fixtures/reviews_title_genre.json'
    # 'python manage.py dumpdata --indent=2 reviews.Title.genres.through -o demo_auth/fixtures/reviews_title_genre.json',
]

for cmd in fixtures_commands:
    subprocess.run(cmd, shell=True, check=True)