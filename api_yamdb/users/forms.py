from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PublicCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Придумайте пароль минимум из 8 символов, в котором должна быть хотя бы одна буква и хотя бы одна цифра'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'bio')

        labels = {
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия',
            'username': 'Ваш логин',
            'email': 'Ваш email',
            'bio': 'О себе'
        }

        help_texts = {
            'first_name': 'Введите ваше имя.',
            'last_name': 'Введите вашу фамилию.',
            'username': 'Придумайте уникальный логин. Не более 150 символов. Это должны быть буквы, цифры и символы @/./+/-/_.',
            'email': 'Введите ваш email.',
            'bio': 'Расскажите о себе.'
        }


class AdminCreationForm(PublicCreationForm):
    class Meta(PublicCreationForm.Meta):
        fields = PublicCreationForm.Meta.fields + ('role',)

        labels = {
            **PublicCreationForm.Meta.labels,
            'role': 'Роль пользователя',  # переопределяем label
        }

        help_texts = {
            **PublicCreationForm.Meta.help_texts,
            'role': 'Выберите роль пользователя.',
        }