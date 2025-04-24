from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_admin_or_superuser(user):
    return (user.is_authenticated and (
        user.is_superuser
        or getattr(user, 'role', '') in ['superuser', 'admin']))


def is_staff(user):
    """Проверяет, является ли пользователь модератором,
    админом или суперюзером"""
    return (user.is_authenticated and (
        user.is_superuser
        or getattr(user, 'role', '') in ['superuser', 'admin', 'moderator']))


def is_author_or_privileged(user, obj=None):
    """Проверяет, является ли пользователь:
    - автором объекта,
    - админом (is_admin),
    - модератором (role='moderator')
    - или суперюзером"""

    # Проверка автора (если передан объект)
    is_author = obj and getattr(obj, 'author', None) == user

    return (
        user.is_authenticated and (
            is_author
            or user.is_superuser
            or getattr(user, 'role', '') in ['superuser', 'admin', 'moderator'])
    )


def is_owner(user, obj=None):
    """Проверяет, является ли пользователь:
    - владельцем объекта (проверяет username)"""

    if hasattr(obj, 'username') and obj.username == user.username:
        return True
    return False


class AuthorOrPrivilegedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return is_author_or_privileged(self.request.user, obj)

    def handle_no_permission(self):
        raise PermissionDenied(
            "Доступ только для авторов или сотрудников сайта")

    @staticmethod
    def check_permission(user, obj):
        """Статический метод для проверки прав без создания экземпляра"""
        return is_author_or_privileged(user, obj)


class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return is_staff(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied(
            "Доступ только для администраторов и модераторов")

    @staticmethod
    def check_permission(user):
        """Статический метод для проверки прав без создания экземпляра"""
        return is_staff(user)


class IsAdminOrSuperuser(UserPassesTestMixin):
    def test_func(self):
        return is_admin_or_superuser(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied("Доступ только для администраторов")

    @staticmethod
    def check_permission(user):
        """Статический метод для проверки прав без создания экземпляра"""
        return is_admin_or_superuser(user)
