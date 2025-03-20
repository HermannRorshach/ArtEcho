import csv


def has_id_field(file_obj):
    try:
        # Проверяем, что первая колонка содержит только целые числа,
        first_column = [int(row[0]) for row in csv.reader(file_obj) if row[0].isdigit()]
        # расположенные в порядке возрастания
        if first_column and first_column == sorted(first_column):
            return True
        return False
    except ValueError:
        return False
