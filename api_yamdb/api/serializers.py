from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ConfirmationCode

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя.")
        return value



from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ConfirmationCodeTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')

        try:
            confirmation = user.confirmation_code
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError('Код подтверждения не найден.')

        if not confirmation.is_valid():
            raise serializers.ValidationError('Срок действия кода истёк.')

        if confirmation.code != code:
            raise serializers.ValidationError('Неверный код подтверждения.')

        tokens = RefreshToken.for_user(user)
        return {
            'access': str(tokens.access_token),
            'refresh': str(tokens),
        }


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'is_active',
            'last_login',
            'is_admin',
            'is_moderator',
            'is_superuser',
        ]
        read_only_fields = [
            'id',
            'is_active',
            'date_joined',
            'last_login',
            'is_admin',
            'is_moderator',
            'is_superuser',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'bio',
        ]