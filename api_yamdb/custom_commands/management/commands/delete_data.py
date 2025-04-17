from django.core.management import call_command
from django.core.management.base import BaseCommand

COMMANDS = [
    ('delete_by_model', 'users.User'),
    ('delete_by_model', 'reviews.Category'),
    ('delete_by_model', 'reviews.Genre'),
    ('delete_by_model', 'reviews.Title'),
    ('delete_by_model', 'reviews.Review'),
    ('delete_by_model', 'reviews.Comment'),
    ('delete_by_table', 'reviews_title_genre'),
]


class Command(BaseCommand):
    """
    Команда для массового удаления данных из таблиц, связанных с
    указанными моделями и таблицами.

    Эта команда последовательно выполняет удаление данных из таблиц,
    используя две команды:
      - `delete_by_model`: для удаления данных из таблицы, найденной
        по имени модели Django.
      - `delete_by_table`: для удаления данных из таблицы,
        найденной по её имени.

    Пример использования:
      python manage.py delete_data

    Список команд и таблиц, из которых удаляются данные, задается в
    переменной COMMANDS. Каждый элемент списка COMMANDS содержит:
    - Название команды (`delete_by_model` или `delete_by_table`).
    - Имя модели или таблицы, из которой будут удалены данные.

    Пример элемента списка COMMANDS для таблицы, соответствующей модели:
      ('delete_by_model', 'users.User')

    Где:
      - `delete_by_model` — команда для удаления данных из таблицы,
        связанной с моделью.
      - 'users.User' — имя модели в формате <app_label>.<model_name>.

    Пример элемента списка COMMANDS для таблицы, найденной по её имени:
      ('delete_by_table', 'reviews_title_genre')

    Где:
      - `delete_by_table` — команда для удаления данных из таблицы,
        найденной по её имени.
      - `reviews_title_genre` — имя таблицы.

    Примечание:
      - Убедитесь, что модели и таблицы существуют в базе данных.
      - Команда удаляет все записи из указанных таблиц, но сами
        таблицы остаются.
    """

    def handle(self, *args, **options):
        """
        Основной метод, который выполняет команду.

        Последовательно вызывает команды для удаления данных из таблиц,
        указанных в переменной COMMANDS.
        """
        for file in COMMANDS:
            call_command(*file)
