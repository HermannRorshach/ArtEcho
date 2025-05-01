from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PublicCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            'Придумайте пароль минимум из 8 символов, '
            'в котором должна быть хотя бы одна буква и хотя бы одна цифра'
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')

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
            'username': (
                'Придумайте уникальный логин. Не более 150 символов. '
                'Это должны быть буквы, цифры и символы @/./+/-/_.'
            ),
            'email': 'Введите ваш email.',
            'bio': 'Расскажите о себе.'
        }


class PublicUpdateForm(PublicCreationForm):

    avatar = forms.ImageField(required=False)
    avatar_clear = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

    def save(self, commit=True):
        print("cleaned_data =", self.cleaned_data)
        user = self.instance
        # Перезагружаем объект из базы данных, чтобы получить актуальные данные
        user.refresh_from_db(fields=['avatar'])

        print('Проверяем старый аватар', user.avatar)
        avatar = self.cleaned_data.get('avatar')
        avatar_clear = self.cleaned_data.get('avatar_clear')

        # Если флаг удаления аватара активирован
        if avatar_clear:
            if user.avatar:
                user.avatar.delete(save=False)  # Удаляем старый аватар
            user.avatar = None  # Обнуляем поле аватара

            if commit:
                User.objects.filter(pk=user.pk).update(avatar=None)
                user.refresh_from_db(fields=['avatar'])
            return user

        # Если загружен новый аватар
        if avatar:
            if user.avatar and user.avatar != avatar:
                user.avatar.delete(save=False)
            user.avatar = avatar

        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'avatar', 'username', 'email', 'first_name', 'last_name', 'bio',
            'birth_date', 'sex', 'city',
            'relationship_status', 'vk_url', 'youtube_url', 'telegram_url',
            'whatsapp_url')

        labels = {
            'avatar': 'Аватар',
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия',
            'bio': 'О себе',
            'birth_date': 'Дата рождения',
            'sex': 'Пол',
            'city': 'Город',
            'relationship_status': 'Семейное положение',
            'vk_url': 'Ссылка на vk',
            'youtube_url': 'Ссылка на канал ютуб',
            'telegram_url': 'Ссылка на телеграм',
            'whatsapp_url': 'Ссылка на whatsapp'
        }

        help_texts = {
            'first_name': 'Введите ваше имя.',
            'last_name': 'Введите вашу фамилию.',
            'username': (
                'Придумайте уникальный логин. Не более 150 символов. '
                'Это должны быть буквы, цифры и символы @/./+/-/_.'
            ),
            'email': 'Введите ваш email.',
            'bio': 'Расскажите о себе.',
            'avatar': 'Загрузите изображение размером не более 5 Мб',
            'birth_date': 'Укажите вашу дату рождения',
            'sex': 'Укажите ваш пол. Изменить в дальнейшем нельзя',
            'city': 'В каком городе вы живёте',
            'relationship_status': 'Расскажите о вашем семейном положении',
        }
