from django.core import management


def reset_demo_data():
    commands = (
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/user.json', 'users_user'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/confirmation_code.json', 'users_confirmationcode'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/category.json', 'reviews_category'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/genre.json', 'reviews_genre'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/title.json', 'reviews_title'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/review.json', 'reviews_review'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/comment.json', 'reviews_comment'),
        ('reset_bd_from_fixtures', 'demo_auth/fixtures/reviews_title_genre.json', 'reviews_title_genre'),

        ('delete_records_with_conditions', 'users_user', 'is_demo=True AND id > 109', '-r'),
        ('delete_records_with_conditions', 'users_confirmationcode', 'is_demo=True', '-r'),
        ('delete_records_with_conditions', 'reviews_category', 'is_demo=True AND id > 6', '-r'),
        ('delete_records_with_conditions', 'reviews_genre', 'is_demo=True AND id > 30', '-r'),
        ('delete_records_with_conditions_by_model', 'reviews.Title', 'is_demo=True, pk__gt=64'),
        ('delete_records_with_conditions', 'reviews_review', 'is_demo=True AND id > 147', '-r'),
        ('delete_records_with_conditions', 'reviews_comment', 'is_demo=True AND id > 19', '-r'),
    )


    for cmd in commands:
        management.call_command(cmd[0], *cmd[1:])
