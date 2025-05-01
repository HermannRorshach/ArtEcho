from django.contrib.auth import get_user_model

from users.forms import PublicCreationForm, PublicUpdateForm

User = get_user_model()


class AdminCreationForm(PublicCreationForm):
    class Meta(PublicCreationForm.Meta):
        fields = PublicCreationForm.Meta.fields + ('role',)

        labels = {
            **PublicCreationForm.Meta.labels,
            'role': 'Роль пользователя',
        }

        help_texts = {
            **PublicCreationForm.Meta.help_texts,
            'role': 'Выберите роль пользователя.',
        }


class AdminUpdateForm(PublicUpdateForm):
    class Meta(PublicUpdateForm.Meta):
        fields = PublicUpdateForm.Meta.fields + ('role', 'username', 'email',)

        labels = {
            **PublicUpdateForm.Meta.labels,
            'role': 'Роль пользователя',
            'username': 'Логин пользователя',
            'email': 'Email пользователя',
        }

        help_texts = {
            **PublicUpdateForm.Meta.help_texts,
            'role': 'Выберите роль пользователя.',
            'username': (
                'Придумайте уникальный логин. Не более 150 символов. '
                'Это должны быть буквы, цифры и символы @/./+/-/_.'
            ),
            'email': 'Введите ваш email.',
        }
