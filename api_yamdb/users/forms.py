from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'bio')

                # Задаем кастомные лейблы для всех полей
        labels = {
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия',
            'username': 'Ваш логин',
            'email': 'Ваш email',
            'bio': 'О себе',
            'role': 'Ваша роль',
        }

        # Задаем кастомные help_text для всех полей
        help_texts = {
            'first_name': 'Введите ваше имя.',
            'last_name': 'Введите вашу фамилию.',
            'username': 'Придумайте уникальный логин. Не более 150 символов. Только английские буквы, цифры и символы @/./+/-/_.',
            'email': 'Введите ваш email.',
            'bio': 'Расскажите о себе.',
            'role': 'Выберите вашу роль.',
        }
