import json
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    """
    Удаляет записи из таблицы базы данных по заданным условиям.

    Аргументы:
    - table_name (str): Название таблицы.
    - conditions (str): Условия для удаления, как в SQL-запросе.
    - --reset-auto-increment: Если передан, сбрасывает счетчик автоинкремента.
    """

    help = 'Удаляет записи из таблицы по заданным условиям и сбрасывает автоинкремент при необходимости.'

    def add_arguments(self, parser):
        parser.add_argument(
            'table_name',
            type=str,
            help='Название таблицы, из которой будут удалены записи.'
        )
        parser.add_argument(
            'conditions',
            type=str,
            help='Условия для удаления записей, как в SQL-запросе.'
        )
        parser.add_argument(
            '--reset-auto-increment',
            '-r',
            action='store_true',
            help='Сбросить счетчик автоинкремента после удаления записей.'
        )

    def handle(self, *args, **options):
        table_name = options['table_name']
        conditions = options['conditions']
        reset_auto_increment = options['reset_auto_increment']

        self.stdout.write(
            self.style.SUCCESS(
                f'Удаление записей из таблицы "{table_name}" по условиям "{conditions}".'
            )
        )

        # Выполняем удаление записей с заданными условиями
        with connection.cursor() as cursor:
            query = f'DELETE FROM {table_name} WHERE {conditions}'
            cursor.execute(query)
            self.stdout.write(self.style.SUCCESS(f'Записи успешно удалены из {table_name}.'))

            # Если флаг установлен, сбрасываем автоинкремент
            if reset_auto_increment:
                self._reset_auto_increment(cursor, table_name)

    def _reset_auto_increment(self, cursor, table_name):
        # Определяем тип базы данных и сбрасываем автоинкремент
        db_name = connection.vendor.lower()

        if db_name == 'postgresql':
            cursor.execute(f'ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;')
            self.stdout.write(self.style.SUCCESS(f'Счетчик автоинкремента для {table_name} сброшен.'))
        elif db_name == 'mysql':
            cursor.execute(f'ALTER TABLE {table_name} AUTO_INCREMENT = 1;')
            self.stdout.write(self.style.SUCCESS(f'Счетчик автоинкремента для {table_name} сброшен.'))
        elif db_name == 'sqlite':
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{table_name}";')
            self.stdout.write(self.style.SUCCESS(f'Счетчик автоинкремента для {table_name} сброшен.'))
        else:
            self.stdout.write(self.style.WARNING('Сброс автоинкремента не поддерживается для данной СУБД.'))
