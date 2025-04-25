from django.views.generic.base import ContextMixin
from django.utils.text import slugify
from transliterate import translit


class DemoAccessMixin:
    """
    Полный контроль демо-доступа для HTML и API:
    - Автоматически добавляет _demo к slug при сохранении
    - Фильтрует queryset
    - Подменяет slug при отображении
    """

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем базовый queryset

        if getattr(self.request.user, 'is_demo', False):
            # Для демо-пользователя - только демо-объекты
            queryset = queryset.filter(is_demo=True)
        else:
            # Для обычных пользователей - только не-демо объекты
            queryset = queryset.exclude(is_demo=True)

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if getattr(self.request.user, 'is_demo', False):
            return queryset.filter(is_demo=True)
        return queryset.exclude(is_demo=True)

    def form_valid(self, form):
        if getattr(self.request.user, 'is_demo', False):
            instance = form.instance
            instance.is_demo = True

            if hasattr(instance, 'slug'):
                self._process_demo_slug(instance)

        return super().form_valid(form)

    def _process_demo_slug(self, instance):
        """Обработка slug для демо-объектов"""

        if hasattr(instance, 'slug') and instance.slug and instance.slug.endswith('_demo'):
            return

        original_slug = getattr(instance, 'slug', '')

        # Генерация slug если пустой
        if not original_slug:
            source_text = (getattr(instance, 'text', '') or
                         getattr(instance, 'name', '') or
                         getattr(instance, 'title', ''))
            original_slug = slugify(translit(source_text[:30], 'ru', reversed=True))

        # Добавляем суффикс
        demo_slug = f"{original_slug}_demo"
        counter = 1

        # Проверка уникальности
        while instance.__class__.objects.filter(slug=demo_slug).exists():
            demo_slug = f"{original_slug}_demo_{counter}"
            counter += 1

        instance.slug = demo_slug

    def perform_create(self, serializer):
        print('Вызываем perform_create')
        user = self.request.user
        print('user =', user)
        instance = serializer.save()
        print('instance =', instance)
        if getattr(user, 'is_demo', False):
            print('Попали в условие, оно выполнилось')
            instance.is_demo = True
            if hasattr(instance, 'slug'):
                self._process_demo_slug(instance)
            instance.save()
        print('в конце метда porform_create instance =', instance)


class DemoFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
