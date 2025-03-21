from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Команда для удаления всех данных из указанной таблицы в базе данных.

    Эта команда выполняет SQL-запрос для удаления всех записей из таблицы,
    имя которой передаётся в качестве аргумента.

    Пример использования:
        python manage.py delete_data reviews_category

    Где:
        - "reviews_category" — имя таблицы в базе данных.

    Примечание:
        - Убедитесь, что имя таблицы указано корректно.
        - Команда удаляет все записи из таблицы, но сама таблица остаётся.
        - Операция выполняется внутри транзакции для обеспечения атомарности.
    """

    help = 'Удаляет данные из таблицы.'

    def add_arguments(self, parser):
        """
        Добавляет аргументы для команды.

        Аргументы:
            - table_name: Имя таблицы, из которой следует удалить данные.
        """
        parser.add_argument(
            'table_name',
            type=str,
            help='Имя модели, экземпляры которой следует удалить из таблицы в БД'
        )

    def handle(self, *args, **options):
        """
        Основной метод, который выполняет команду.

        Получает имя таблицы и выполняет SQL-запрос для удаления всех записей из неё.
        Операция выполняется внутри транзакции для обеспечения атомарности.

        Аргументы:
            - options: Словарь с переданными аргументами командной строки.
        """
        table_name = options['table_name']

        self.stdout.write(self.style.SUCCESS(f'Подготавливаем данные к удалению из таблицы "{table_name}"'))
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table_name}")
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно удалили объекты модели {table_name} из соответствующей таблицы'))
