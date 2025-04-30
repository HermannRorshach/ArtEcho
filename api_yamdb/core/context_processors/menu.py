def menu(request):
    items = {
        'common_items': [
            {'path': 'api:schema-redoc', 'text': 'API'},
            {'path': 'reviews:contacts', 'text': 'Техподдержка'},
            {'path': 'reviews:faq', 'text': 'FAQ'},
        ],
    }
    if request.user.is_authenticated:
        items['authenticated_items'] = [
            {
                'path': 'users:password_change',
                'text': 'Изменить пароль',
                'link_light': True
            },
            {
                'path': 'users:me',
                'text': 'Профиль',
                'link_light': True
            },
        ]
    else:
        items['guest_items'] = [
            {'path': 'users:login', 'text': 'Войти'},
            {'path': 'users:signup', 'text': 'Регистрация'},
        ]
    return items
