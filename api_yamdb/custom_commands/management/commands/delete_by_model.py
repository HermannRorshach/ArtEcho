from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Команда для удаления всех данных из таблицы, связанной с указанной моделью.

    Эта команда находит таблицу по имени модели и удаляет все записи из неё.
    Имя модели передаётся в формате <app_label>.<model_name>.

    Пример использования:
      python manage.py delete_data reviews.Category

    Где:
      - `reviews` — имя приложения (app_label).
      - `Category` — имя модели (model_name).

    Примечание:
      - Убедитесь, что модель существует в указанном приложении.
      - Команда удаляет все записи из таблицы, связанной с моделью.
      - После удаления данных таблица остаётся пустой, но сама таблица
        не удаляется.
    """

    help = 'Удаляет данные из таблицы, находя её по имени модели.'

    def add_arguments(self, parser):
        """
        Добавляет аргументы для команды.

        Аргументы:
            - model_name: Имя модели в формате <app_label>.<model_name>.
        """
        parser.add_argument(
            'model_name',
            type=str,
            help=('Имя модели, экземпляры которой следует удалить '
                  'из таблицы в БД')
        )

    def handle(self, *args, **options):
        """
        Основной метод, который выполняет команду.

        Получает имя модели, находит соответствующую таблицу в базе данных
        и удаляет все записи из неё.

        Аргументы:
            - options: Словарь с переданными аргументами командной строки.
        """
        app_name, model_name = options['model_name'].split('.')

        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            raise CommandError(f'Model "{model_name}" not found.')

        self.stdout.write(
            self.style.SUCCESS(
                f'Подготавливаем данные к удалению из таблицы для '
                f'модели "{model_name}"'))
        model.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно удалили объекты модели {model_name} '
                f'из соответствующей таблицы'))
