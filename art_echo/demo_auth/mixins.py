from django.utils.text import slugify
from transliterate import translit


class DemoAccessMixin:
    """
    Миксин для поддержки логики 'демо-доступа' в HTML-представлениях
    и DRF API.

    Поведение:
    - Фильтрует queryset в зависимости от роли пользователя:
        - Демо-пользователи получают только объекты с is_demo=True
        - Обычные пользователи получают объекты без is_demo
    - Автоматически помечает создаваемые объекты как демо
      (is_demo=True) для демо-пользователей
    - Автоматически формирует уникальный slug с суффиксом
      `_demo` при создании объектов

    Поддерживает:
    - Django CBV: ListView, CreateView, UpdateView
    - Django REST Framework: GenericAPIView, CreateModelMixin и т.п.

    Требования к модели:
    - Наличие булевого поля `is_demo`
    - (Опционально) наличие поля `slug` для формирования slug

    Использование:
        1. Унаследуйте представление от DemoAccessMixin.
        2. Убедитесь, что у вашей модели есть поле `is_demo`.
        3. При необходимости реализуйте свой get_queryset
           и вызовите self.filter_queryset(queryset).

    Пример:
        class ReviewListView(DemoAccessMixin, ListView):
            model = Review

            def get_queryset(self):
                queryset = Review.objects.filter(...)
                return self.filter_queryset(queryset)
    """

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем базовый queryset

        if getattr(self.request.user, 'is_demo', False):
            # Для демо-пользователя - только демо-объекты
            return queryset.filter(is_demo=True)
        # Для обычных пользователей - только не-демо объекты
        return queryset.exclude(is_demo=True)

    def filter_queryset(self, queryset):
        if getattr(self.request.user, 'is_demo', False):
            return queryset.filter(is_demo=True)
        return queryset.exclude(is_demo=True)

    def form_valid(self, form):
        if (
            hasattr(form, 'instance')
            and getattr(self.request.user, 'is_demo', False)
        ):
            instance = form.instance
            instance.is_demo = True

            if hasattr(instance, 'slug'):
                self._process_demo_slug(instance)

        return super().form_valid(form)

    def _process_demo_slug(self, instance):
        """Обработка slug для демо-объектов"""

        if (
            hasattr(instance, 'slug')
            and instance.slug and instance.slug.endswith('_demo')
        ):
            return

        original_slug = getattr(instance, 'slug', '')

        # Генерация slug если пустой
        if not original_slug:
            source_text = (
                getattr(instance, 'text', '')
                or getattr(instance, 'name', '')
                or getattr(instance, 'title', '')
            )
            original_slug = slugify(
                translit(source_text[:30], 'ru', reversed=True))

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

    def _maybe_set_demo(self, instance):
        if getattr(self.request.user, 'is_demo', False):
            instance.is_demo = True
            if hasattr(instance, 'slug'):
                self._process_demo_slug(instance)
            instance.save()


class DemoFormMixin:
    """
    Миксин для передачи текущего пользователя (`request.user`)
    в форму через kwargs.

    Назначение:
    -----------
    Обеспечивает доступ к пользователю внутри формы, чтобы можно было
    адаптировать поведение формы в зависимости от прав пользователя
    (например, от `is_demo`), без необходимости переопределять
    каждый раз `get_form_kwargs`.

    Особенно полезен в связке с `DemoModelForm`, который фильтрует
    доступные значения в полях типа ModelChoiceField
    и ModelMultipleChoiceField на основе пользователя.

    Использование:
    --------------
    Просто добавьте миксин к классу-представлению (например, CreateView):

        class MyCreateView(DemoFormMixin, CreateView):
            form_class = MyForm

    Или совместно с `DemoAccessMixin`:

        class MyCreateView(
            DemoAccessMixin, DemoFormMixin, CreateView
        ):
            ...

    Совместное использование:
    -------------------------
    - `DemoAccessMixin` отвечает за фильтрацию queryset и генерацию
      slug для демо-объектов.
    - `DemoFormMixin` передаёт пользователя в форму.
    - Вместе они позволяют реализовать полноценную поддержку
      демо-доступа как в представлении, так и в формах.

    Важно:
    ------
    Порядок наследования имеет значение. Чтобы `DemoFormMixin`
    корректно переопределил `get_form_kwargs`, он должен быть
    указан **до** базового класса вьюхи (например, CreateView).
    Рекомендуется придерживаться следующего порядка:
        DemoAccessMixin, DemoFormMixin, ViewClass

    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
