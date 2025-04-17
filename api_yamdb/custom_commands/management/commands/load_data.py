from django.core.management import call_command
from django.core.management.base import BaseCommand

FILES = [
    ('import_by_model', 'static/data/users.csv', 'users.User', '-b'),
    (
        'import_by_model', 'static/data/category.csv',
        'reviews.Category', '--bulk'),
    ('import_by_model', 'static/data/genre.csv', 'reviews.Genre'),
    ('import_by_model', 'static/data/titles.csv', 'reviews.Title'),
    ('import_by_model', 'static/data/review.csv', 'reviews.Review'),
    ('import_by_model', 'static/data/comments.csv', 'reviews.Comment'),
    ('import_by_table', 'static/data/genre_title.csv', 'reviews_title_genre'),
]


class Command(BaseCommand):
    """
    Команда для массового импорта данных из CSV и JSON-файлов в базу данных.

    Эта команда последовательно выполняет импорт данных из указанных файлов
    в соответствующие модели Django. Используются две команды:
    - `import_by_model`: для импорта данных в таблицу, найденную по
      модели Django.
    - `import_by_table`: для импорта данных в таблицу по её имени.

    Пример использования:
        python manage.py load_data

    Список файлов и моделей, в которые импортируются данные, задается в
    переменной FILES.
    Каждый элемент списка FILES содержит:
    - Название команды (`import_by_model` или `import_by_table`).
    - Путь к файлу (CSV или JSON).
    - Имя модели или таблицы, в которую будут импортированы данные.
    - Опционально: флаг `-b` или `--bulk` для команды `import_by_model`,
      который указывает на использование массовой вставки данных с помощью
      `bulk_create`.
      Если флаг не указан, данные вставляются по одному объекту с вызовом
      метода `save()`.

    Пример элемента списка FILES без флага:
        ('import_by_model', 'static/data/users.csv', 'users.User')

    Пример элемента списка FILES с флагом `-b`:
        ('import_by_model', 'static/data/users.csv', 'users.User', '--bulk')

    Где:
        - 'import_by_model' — команда для импорта данных в модель.
        - 'static/data/users.csv' — путь к CSV-файлу.
        - 'users.User' — имя модели в формате <app_label>.<model_name>.
        - '-b' — флаг для массовой вставки данных.

    Примечание:
        - Убедитесь, что файлы (CSV или JSON) находятся в указанных путях.
        - Модели и таблицы должны быть корректно настроены в Django.
        - Команда автоматически определяет формат файла (CSV или JSON)
          по его расширению.
    """

    def handle(self, *args, **options):
        """
        Основной метод, который выполняет команду.

        Последовательно вызывает команды для импорта данных из файлов,
        указанных в переменной FILES. Поддерживаются как CSV, так и JSON-файлы.

        Команда `import_by_model` поддерживает флаг `-b` или `--bulk`,
        чтобы включить вставку данных массово с помощью `bulk_create`.
        """
        for file in FILES:
            call_command(*file)
