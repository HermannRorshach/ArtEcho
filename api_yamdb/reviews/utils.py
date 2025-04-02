from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_admin_or_superuser(user):
    return user.is_admin or user.is_superuser


def is_staff(user):
    """Проверяет, является ли пользователь модератором, админом или суперюзером"""
    return user.is_superuser or getattr(user, 'role', '') in ['admin', 'moderator']



def is_author_or_privileged(user, obj=None):
    """Проверяет, является ли пользователь:
    - автором объекта,
    - админом (is_admin),
    - модератором (role='moderator')
    - или суперюзером"""

    # Проверка автора (если передан объект)
    is_author = obj and getattr(obj, 'author', None) == user

    return (
        is_author or
        user.is_superuser or
        getattr(user, 'role', '') in ['admin', 'moderator']
    )



class AuthorOrPrivilegedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return is_author_or_privileged(self.request.user, obj)

    def handle_no_permission(self):
        raise PermissionDenied("Доступ только для авторов или сотрудников сайта")


class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return is_staff(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied("Доступ только для администраторов и модераторов")


class IsAdminOrSuperuser(UserPassesTestMixin):
    def test_func(self):
        return is_admin_or_superuser(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied("Доступ только для администраторов")