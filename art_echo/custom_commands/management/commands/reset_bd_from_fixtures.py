import json

from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    """
    Обновляет данные в таблице на основе JSON-фикстуры.

    Функциональность:
    - Обновляет существующие записи по pk.
    - Создает новые записи, если их нет.
    - Не трогает записи в таблице, которых нет в фикстуре.

    Аргументы:
    - file_path (str): Путь к файлу фикстуры (JSON).
    - table_name (str): Название таблицы, в которую вносить изменения.

    Логика работы:
    - Загружает данные из JSON-файла.
    - Для каждой записи: обновляет существующую или создаёт новую.

    Возможные ошибки:
    - Если формат файла не JSON, команда выдаст ошибку.
    - Если таблица или модель не найдены, команда выдаст ошибку.

    Вывод:
    - Подтверждение успешного обновления данных.
    """
    help = ('Обновляет данные в таблице из фикстуры (JSON). '
            'Обновляет записи по pk или создает их, не удаляя другие записи.')

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к JSON-файлу с фикстурой.'
        )
        parser.add_argument(
            'table_name',
            type=str,
            help='Название таблицы базы данных.'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        table_name = options['table_name']

        self.stdout.write(
            self.style.SUCCESS(
                f'Обновление таблицы "{table_name}" из фикстуры "{file_path}".'
            )
        )

        if not file_path.endswith('.json'):
            raise CommandError('Поддерживается только формат JSON.')

        with open(file_path, mode='r', encoding='utf-8') as f:
            fixtures = json.load(f)

        if not fixtures:
            self.stdout.write(self.style.WARNING('Фикстура пуста.'))
            return

        with connection.cursor() as cursor:
            for obj in fixtures:
                fields = []
                values = []
                updates = []
                for field, value in obj['fields'].items():
                    fields.append(field)
                    values.append(value)
                    updates.append(f"{field} = EXCLUDED.{field}")

                fields.insert(0, 'id')
                values.insert(0, obj['pk'])
                updates.insert(0, "id = EXCLUDED.id")

                placeholders = ', '.join(['%s'] * len(fields))
                columns = ', '.join(fields)
                update_clause = ', '.join(updates)

                query = (
                    f'INSERT INTO {table_name} ({columns}) '
                    f'VALUES ({placeholders}) '
                    f'ON CONFLICT (id) DO UPDATE SET {update_clause}'
                )
                cursor.execute(query, values)

        self.stdout.write(
            self.style.SUCCESS(
                f'Таблица {table_name} успешно обновлена из {file_path}.')
        )
