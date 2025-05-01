from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Удаляет записи из указанной модели по заданным условиям,
    включая связанные данные в промежуточных таблицах ManyToMany.

    Аргументы:
            model_name (str): Полное имя модели в формате 'app_label.ModelName'
        (например, 'reviews.Title')
            conditions (str): Условия фильтрации в формате
        'field1=value1, field2__lookup=value2'

    Опции:
        --help, -h: Показать это сообщение и выйти

    Примеры использования:
        Базовый пример:
            python manage.py delete_records_with_conditions_by_model reviews.Title 'is_demo=True, pk__gt=64'
            Удалит все записи Title, где is_demo=True и id больше 64

        Сложные условия:
            python manage.py delete_records_with_conditions_by_model auth.User 'is_active=False, last_login__lt="2023-01-01"'
            Удалит неактивных пользователей, не заходивших с 2023 года

            python manage.py delete_records_with_conditions_by_model shop.Order 'status="cancelled", created_at__year=2022'
            Удалит все отмененные заказы за 2022 год

        Использование различных lookup-ов:
            python manage.py delete_records_with_conditions_by_model blog.Post 'title__contains="draft", publish_date__isnull=True'
            Удалит черновики постов
            (с "draft" в заголовке и без даты публикации)

    Особенности:
    1. Поддерживает все стандартные lookups Django
       (__gt, __lt, __contains и т.д.)
    2. Автоматически обрабатывает связанные ManyToMany поля -
       удаляет записи из промежуточных таблиц
    3. Поддерживает различные типы значений:
    - Строки (в одинарных или двойных кавычках)
    - Числа (целые и с плавающей точкой)
    - Булевы значения (True/False)
    - None (как 'null' или 'None')
    4. Выводит количество удаленных записей

    Обработка ошибок:
    - Если модель не найдена, выводит сообщение об ошибке
    - Если условия имеют неверный формат, выводит сообщение об ошибке
    - Если не найдено ни одной записи для удаления, выводит предупреждение

    Особенности удаления:
    - Для обычных моделей выполняется эффективное массовое удаление
      через SQL DELETE
    - Для моделей с M2M-связями:
    * Django сам обрабатывает удаление промежуточных записей через
      сигналы модели.
    * Затем удаляются сами объекты
    * Вызываются сигналы pre_delete/post_delete для каждого объекта
    - Операция не является атомарной.
    """

    help = ('Удаляет записи из модели и связанных промежуточных '
            'таблиц Many-to-Many или саму модель без таких связей.')

    def add_arguments(self, parser):
        parser.add_argument(
            'model_name',
            type=str,
            help='Название модели, из которой будут удалены записи.'
        )
        parser.add_argument(
            'conditions',
            type=str,
            help='Условия для удаления записей, как в фильтре Django ORM.'
        )

    def handle(self, *args, **options):
        app_name, model_name = options['model_name'].split('.')
        conditions = options['conditions']

        self.stdout.write(
            self.style.SUCCESS(
                f'Удаление записей из модели "{model_name}" '
                f'с условиями "{conditions}".'
            )
        )

        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            raise CommandError(f'Model "{model_name}" not found.')

        try:
            condition_dict = self._parse_conditions_dict(conditions)
        except Exception as e:
            raise CommandError(f'Ошибка разбора условий: {e}')

        records_to_delete = model.objects.filter(**condition_dict)
        deleted_count = records_to_delete.count()

        if deleted_count > 0:
            records_to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'{deleted_count} записей успешно удалены из '
                    f'модели "{model_name}".'
                ))
        else:
            self.stdout.write(
                self.style.WARNING('Записи для удаления не найдены.'))

    def _parse_conditions_dict(self, conditions):
        """Парсит строку условий в словарь для .filter()."""

        import ast

        condition_dict = {}
        pairs = [
            pair.strip() for pair in conditions.split(',') if pair.strip()
        ]
        for pair in pairs:
            if '=' not in pair:
                raise ValueError(
                    f'Неверный формат условия: "{pair}". Ожидался "=".')

            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Обработка null/None вручную
            if value.lower() in ('null', 'none'):
                value = None
            else:
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass  # оставить строкой как есть

            condition_dict[key] = value

        return condition_dict
