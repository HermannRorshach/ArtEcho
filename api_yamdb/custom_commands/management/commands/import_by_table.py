from django.core.management.base import BaseCommand, CommandError
import csv
import json
from django.db import connection, IntegrityError
from django.db.utils import ProgrammingError
from custom_commands.utils import has_id_field

class Command(BaseCommand):
    """
    Импортирует данные из CSV или JSON файла в указанную таблицу базы данных.

    Функциональность:
    - Поддерживает два формата файлов: CSV и JSON.
    - Позволяет загружать данные с явным указанием id или без него.
    - Если в файле есть поле id и оно не конфликтует с уже существующими записями в таблице,
    данные сохраняются с указанными id.
    - Если в файле есть поле id, но некоторые значения уже присутствуют в таблице,
    все id в файле игнорируются и заменяются автоматически.
    - Если поле id в файле отсутствует, оно будет автоматически присвоено при вставке данных.
    - В CSV файле заголовки не обязательны. Если они присутствуют, программа их распознает.
    Если их нет, используется порядок полей таблицы.
    - Если в CSV файле отсутствуют заголовки, программа проверяет, является ли первый столбец
    полем id. Если первый столбец содержит только численные значения в порядке
    возрастания, программа считает этот столбец полем id.

    Аргументы:
    - file_path (str): Абсолютный или относительный путь к файлу с данными (CSV или JSON).
    Относительный путь строится от директории, содержащей `manage.py`.
    - table_name (str): Имя таблицы в базе данных, в которую нужно загрузить данные.

    Логика работы:
    - Определяет расширение файла и выбирает соответствующий метод обработки.
    - Читает данные, корректирует id при необходимости.
    - Если CSV файл не содержит заголовков, проверяет первый столбец на наличие id.
    - Использует SQL-запросы для вставки данных в базу.

    Возможные ошибки:
    - Если указанная таблица не найдена, программа выдаст ошибку.
    - Если формат файла не поддерживается, программа выдаст ошибку.
    - Если id в файле конфликтуют с существующими в базе, они заменяются автоматически.

    Вывод:
    - При успешном импорте выводит сообщение с указанием таблицы и файла.
    - Если id были изменены, выводит предупреждение.
    """
    help = 'Импортирует данные из файла в указанную таблицу. Поддерживаются форматы CSV и JSON.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к файлу (CSV или JSON), из которого нужно импортировать данные.'
        )
        parser.add_argument(
            'table_name',
            type=str,
            help='Имя таблицы, в которую следует записать данные.'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        table_name = options['table_name']

        self.stdout.write(self.style.SUCCESS(f'Импорт данных в таблицу "{table_name}" из файла "{file_path}".'))

        file_extension = file_path.split('.')[-1]

        if file_extension == 'csv':
            self.import_csv_data(file_path, table_name)
        elif file_extension == 'json':
            self.import_json_data(file_path, table_name)
        else:
            raise CommandError(f'Unsupported file format: {file_extension}')

    def get_table_columns(self, table_name):
        with connection.cursor() as cursor:
            if connection.vendor == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table_name})")
                return [row[1] for row in cursor.fetchall()]  # row[1] содержит имя столбца
            else:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE LOWER(table_name) = LOWER(%s)", [table_name])
                return [row[0] for row in cursor.fetchall()]


    def import_csv_data(self, file_path, table_name):
        with open(file_path, mode='r', encoding='utf-8') as f:
            table_fields = self.get_table_columns(table_name)
            reader = csv.reader(f)
            first_row = next(reader)
            is_it_header = set(first_row) <= set(table_fields)
            if is_it_header:
                fields = first_row
            else:
                fields = table_fields
                f.seek(0)
                has_id = has_id_field(f)
                f.seek(0)
                if not has_id:
                    table_fields.pop(0)
            data_list = []
            for row in reader:
                data = {field: value for field, value in zip(fields, row)}
                data_list.append(data)

            self.insert_data(table_name, data_list)

            self.stdout.write(
                self.style.WARNING('Некоторые id, указанные в файле, уже существуют '
                                    'в базе данных. id при записи данных были заменены'
                                    ' автоматически.'))


    def import_json_data(self, file_path, table_name):
        with open(file_path, mode='r', encoding='utf-8') as f:
            data_list = json.load(f)
        self.insert_data(table_name, data_list)

    def insert_data(self, table_name, data_list):
        with connection.cursor() as cursor:
            fields = data_list[0].keys()
            placeholders = ', '.join(['%s'] * len(fields))
            columns = ', '.join(fields)
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            try:
                cursor.executemany(query, [tuple(d.values()) for d in data_list])
            except IntegrityError:
                fields = [field for field in data_list[0].keys() if field != "id"]
                placeholders = ', '.join(['%s'] * len(fields))
                columns = ', '.join(fields)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                for data in data_list:
                    data.pop('id', None)
                cursor.executemany(query, [tuple(d.values()) for d in data_list])
                self.stdout.write(self.style.WARNING('Некоторые id уже существуют. id были заменены автоматически.'))
        self.stdout.write(self.style.SUCCESS(f'Успешно импортировано в таблицу {table_name}'))
