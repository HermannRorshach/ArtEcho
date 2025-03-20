from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
import json
from django.db import IntegrityError
from custom_commands.utils import has_id_field

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Импортирует данные из CSV или JSON файла в указанную модель Django.

    Функциональность:
    - Поддерживает два формата файлов: CSV и JSON.
    - Позволяет загружать данные с явным указанием id или без него.
    - Если в файле есть поле id и оно не конфликтует с уже существующими записями в таблице,
      данные сохраняются с указанными id.
    - Если в файле есть поле id, но некоторые значения уже присутствуют в таблице,
      все id в файле игнорируются и заменяются автоматически.
    - Если поле id в файле отсутствует, оно будет автоматически присвоено при вставке данных.
    - В CSV файле заголовки не обязательны. Если они присутствуют, программа их распознает.
      Если их нет, используется порядок полей модели.
    - Если в CSV файле отсутствуют заголовки, программа проверяет, является ли первый столбец
      полем id. Если первый столбец содержит только численные значения в порядке
      возрастания, программа считает этот столбец полем id.

    Аргументы:
    - file_path (str): Абсолютный или относительный путь к файлу с данными (CSV или JSON).
      Относительный путь строится от директории, содержащей `manage.py`.

    - model_name (str): Полное имя модели Django в формате "app_name.ModelName", в которую нужно загрузить данные.

    Логика работы:
    - Определяет расширение файла и выбирает соответствующий метод обработки.
    - Читает данные, корректирует id при необходимости.
    - Если CSV файл не содержит заголовков, проверяет первый столбец на наличие id.
    - Использует bulk_create для вставки данных в базу.

    Возможные ошибки:
    - Если указанная модель не найдена, программа выдаст ошибку.
    - Если формат файла не поддерживается, программа выдаст ошибку.
    - Если id в файле конфликтуют с существующими в базе, они заменяются автоматически.

    Вывод:
    - При успешном импорте выводит сообщение с указанием модели и файла.
    - Если id были изменены, выводит предупреждение.
    """

    help = 'Импортирует данные из файла в указанную модель. Поддерживаются форматы CSV и JSON.'

    def add_arguments(self, parser):
        # Добавление аргумента для файла
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к файлу (CSV или JSON), из которого нужно импортировать данные.'
        )
        # Добавление аргумента для модели
        parser.add_argument(
            'model_name',
            type=str,
            help='Имя модели, в которую следует записать данные.'
        )

    def handle(self, *args, **options):
        # Логика обработки данных будет реализована позже.
        file_path = options['file_path']
        app_name, model_name = options['model_name'].split(".")

        # Попробуем получить модель по имени
        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            raise CommandError(f'Model "{model_name}" not found.')

        self.stdout.write(self.style.SUCCESS(f'Preparing to import data into model "{model_name}" from file "{file_path}".'))

        # Проверим расширение файла для выбора метода обработки
        file_extension = file_path.split('.')[-1]

        if file_extension == 'csv':
            self.import_csv_data(file_path, model)
        elif file_extension == 'json':
            self.import_json_data(file_path, model)
        else:
            raise CommandError(f'Unsupported file format: {file_extension}')

    def insert_data(self, data_list, model):
        try:
            objects = [model(**data) for data in data_list]
            model.objects.bulk_create(objects)
        except IntegrityError:
            for data in data_list:
                data.pop("id")
            objects = [model(**data) for data in data_list]
            model.objects.bulk_create(objects)
            self.stdout.write(
                self.style.WARNING('Некоторые id, указанные в файле, уже существуют '
                                'в базе данных. id при записи данных были заменены'
                                ' автоматически.'))

    def import_csv_data(self, file_path, model):
        with open(file_path, mode='r', encoding='utf-8') as f:
            model_fields = [field.attname for field in model._meta.get_fields() if hasattr(field, 'attname')]
            reader = csv.reader(f)
            first_row = next(reader)
            is_it_header = set(first_row) <= set(model_fields)

            if is_it_header:
                fields = first_row
            else:
                fields = model_fields
                f.seek(0)
                has_id = has_id_field(f)
                f.seek(0)
                if not has_id:
                    model_fields.pop(0)
            data_list = []

            for row in reader:
                data = {field: value for field, value in zip(fields, row)}
                data_list.append(data)
        self.insert_data(data_list, model)
        self.stdout.write(self.style.SUCCESS(f'Успешно импортировали {file_path} в модель {model.__name__}'))

    def import_json_data(self, file_path, model):
        with open(file_path, mode='r', encoding="utf-8") as f:
            data_list = json.load(f)

        self.insert_data(data_list, model)
        self.stdout.write(self.style.SUCCESS(f'Успешно импортировали {file_path} в модель {model.__name__}'))
