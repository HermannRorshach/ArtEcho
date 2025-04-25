import re
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import (Category, Comment, Genre, Review,
                            Title)
from users.models import ConfirmationCode
User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        # Проверка на зарезервированное имя
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.')

        # Проверка формата username
        if not re.fullmatch(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                'Имя пользователя содержит недопустимые символы')

        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email).exists():
            if not User.objects.filter(email=email, username=username).exists(
            ):
                raise serializers.ValidationError(
                    {'email': (f'Пользователь с email {email} '
                               f'зарегистрирован с другим username')}
                )
        else:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {'email': (f'Username {username} уже занят, '
                               f'придумайте другой')}
                )
        return data


class ConfirmationCodeTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы'
            )
        ]
    )
    confirmation_code = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = None

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            error = serializers.ValidationError(
                {'detail': 'Пользователь не найден'},
                code='not_found'
            )
            self.error_code = 'not_found'  # Добавляем код ошибки
            raise error

        try:
            confirmation = user.confirmation_code
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'Код подтверждения не найден'},
                code='invalid'
            )

        if not confirmation.is_valid():
            raise serializers.ValidationError(
                {'detail': 'Срок действия кода истёк'},
                code='invalid'
            )

        if confirmation.code != code:
            raise serializers.ValidationError(
                {'detail': 'Неверный код подтверждения'},
                code='invalid'
            )

        tokens = RefreshToken.for_user(user)
        return {
            'access': str(tokens.access_token),
            'refresh': str(tokens),
        }


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'id',
            'sex',
            'birth_date',
            'city',
            'relationship_status',
            'vk_url',
            'youtube_url',
            'telegram_url',
            'whatsapp_url'
        ]
        read_only_fields = [
            'id',
            'is_active',
            'last_login',
            'is_admin',
            'is_moderator',
            'is_superuser',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы'
            )]
    )
    email = serializers.CharField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'sex',
            'birth_date',
            'city',
            'relationship_status',
            'vk_url',
            'youtube_url',
            'telegram_url',
            'whatsapp_url'
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
            'sex': {'required': False},
            'birth_date': {'required': False},
            'bio': {'required': False},
            'city': {'required': False},
            'relationship_status': {'required': False},
            'vk_url': {'required': False},
            'youtube_url': {'required': False},
            'telegram_url': {'required': False},
            'whatsapp_url': {'required': False}
        }


class UserAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы'
            )]
    )
    email = serializers.CharField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
            'role': {'required': False},
        }


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=50,)

    class Meta:
        model = Category
        fields = ['name', 'slug']

        extra_kwargs = {
            'slug': {'required': False},
        }

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Категория с таким slug уже существует')
        return value


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        max_length=50,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        model = Genre
        fields = ['name', 'slug']

        extra_kwargs = {
            'slug': {'required': False},
        }

    def validate_slug(self, value):
        if Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Жанр с таким slug уже существует')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category', 'slug'
        )

    def get_rating(self, obj):
        return obj.average_rating

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')
        return value


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'slug'
        )

        extra_kwargs = {
            'id': {'read_only': True},
            'description': {'required': False},
            'slug': {'required': False},
        }

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')
        return value


class GetReviewSerializer(serializers.ModelSerializer):
    title = GetTitleSerializer()
    # author = UserDetailSerializer()
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Review
        fields = (
            'id', 'title', 'text', 'author', 'score',
            'pub_date', 'update_date', 'slug')


class ReviewWriteSerializer(GetReviewSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'score')

        extra_kwargs = {
            'id': {'read_only': True},
        }


class GetCommentSerializer(serializers.ModelSerializer):
    review = GetReviewSerializer()
    # author = UserDetailSerializer()
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Comment
        fields = (
            'id', 'review', 'text', 'pub_date',
            'update_date', 'author', 'slug')


class CommentWriteSerializer(GetReviewSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')

        extra_kwargs = {
            'id': {'read_only': True},
        }
