from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    bio = models.TextField(max_length=250, blank=True, null=True)
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
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"pk": self.pk})
