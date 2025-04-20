from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f'Confirmation code for {self.user.username}'


def user_avatar_path(instance, filename):
    return f'users/{instance.username}/avatars/{filename}'


class User(AbstractUser):
    bio = models.TextField(
        max_length=250, blank=True, null=True,
        verbose_name='Несколько строк о себе')
    ROLE_CHOICES = [
        ('admin', 'Админ'),
        ('moderator', 'Модератор'),
        ('superuser', 'Супер-юзер'),
        ('user', 'Авторизованный пользователь'),
    ]
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль на сайте'
    )

    email = models.EmailField(
        unique=True, blank=False, verbose_name='Email')

    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    SEX_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]

    sex = models.CharField(
        max_length=7,
        choices=SEX_CHOICES,
        blank=True,
        null=True,
        verbose_name='Пол'
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Город'
    )

    RELATIONSHIP_STATUS_CHOICES = [
        ('married', 'Женат/Замужем'),
        ('in_relationship', 'В отношениях'),
        ('searching', 'В поиске'),
    ]

    relationship_status = models.CharField(
        max_length=16,
        choices=RELATIONSHIP_STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='Семейное положение'
    )

    vk_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на ВКонтакте'
    )

    youtube_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на YouTube'
    )

    telegram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на Telegram'
    )

    whatsapp_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на WhatsApp'
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def get_absolute_url(self):
        return reverse('users:user_detail', kwargs={'username': self.username})

    def get_admin_url(self):
        return reverse(
            'admin_office:admin_user_detail', kwargs={'username': self.username})
