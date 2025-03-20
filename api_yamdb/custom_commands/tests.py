import pytest
from django.core.management import call_command
from django.db import connection, transaction

TEST_CASES = [
    ("static/data/category_with_header_and_id_1.csv", [[1, "Фильм", "movie"], [2, "Книга", "book"], [3, "Музыка", "music"]]),
    ("static/data/category_with_header_and_id_2.csv", [[2, "Фильм", "movie"], [3, "Книга", "book"], [5, "Музыка", "music"]]),
    ("static/data/category_with_header_and_id_3.csv", [[2, "Фильм", "movie"], [3, "Книга", "book"], [5, "Музыка", "music"]]),
    ("static/data/category_with_id1.csv", [[1, "Фильм", "movie"], [2, "Книга", "book"], [3, "Музыка", "music"]]),
    ("static/data/category_with_id2.csv", [[2, "Фильм", "movie"], [3, "Книга", "book"], [5, "Музыка", "music"]]),
    ("static/data/category_without_id.csv", [[1, "Фильм", "movie"], [2, "Книга", "book"], [3, "Музыка", "music"]]),
    ("static/data/category_with_id1.json", [[1, "Фильм", "movie"], [2, "Книга", "book"], [3, "Музыка", "music"]]),
    ("static/data/category_with_id2.json", [[2, "Фильм", "movie"], [3, "Музыка", "music"], [5, "Книга", "book"]]),
    ("static/data/category_without_id.json", [[1, "Фильм", "movie"], [2, "Книга", "book"], [3, "Музыка", "music"]]),
]

@pytest.fixture(params=TEST_CASES)
def test_case(request):
    return request.param

@pytest.fixture(autouse=True)
def clean_reviews_category():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM reviews_category")
    yield


@pytest.mark.django_db(transaction=True)
def test_import_by_table(test_case):
    csv_file, expected_data = test_case

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO reviews_category (name, slug) VALUES (%s, %s)", ["Без категории", "without_category"])

    with connection.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(id), 0) FROM reviews_category")
        last_id_before = cursor.fetchone()[0]

    if expected_data[0][0] <= last_id_before:
        difference = last_id_before + 1 - expected_data[0][0]
        expected_data = [[data[0] + difference, data[1], data[2]] for data in expected_data]

    try:
        call_command('import_by_table', csv_file, 'reviews_category')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reviews_category WHERE id > %s", [last_id_before])
            added_rows = cursor.fetchall()

        assert len(added_rows) == len(expected_data)
        assert all(added == tuple(expected) for added, expected in zip(added_rows, expected_data))

    finally:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reviews_category")
                cursor.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'reviews_category'")


@pytest.mark.django_db(transaction=True)
def test_import_by_model(test_case):
    csv_file, expected_data = test_case

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO reviews_category (name, slug) VALUES (%s, %s)", ["Без категории", "without_category"])

    with connection.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(id), 0) FROM reviews_category")
        last_id_before = cursor.fetchone()[0]

    if expected_data[0][0] <= last_id_before:
        difference = last_id_before + 1 - expected_data[0][0]
        expected_data = [[data[0] + difference, data[1], data[2]] for data in expected_data]

    try:
        call_command('import_by_model', csv_file, 'reviews.Category')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reviews_category WHERE id > %s", [last_id_before])
            added_rows = cursor.fetchall()

        assert len(added_rows) == len(expected_data)
        assert all(added == tuple(expected) for added, expected in zip(added_rows, expected_data))

    finally:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM reviews_category")
                cursor.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'reviews_category'")
