from django import forms


class DemoModelForm(forms.ModelForm):
    """
    Базовая форма для поддержки демо-доступа в админских формах.

    Назначение:
    -----------
    Автоматически ограничивает выбор в полях типа ModelChoiceField
    и ModelMultipleChoiceField, если текущий пользователь является
    демо-пользователем.

    Для всех таких полей, связанных с моделями, содержащими булево
    поле `is_demo`, происходит фильтрация queryset'а: пользователю
    доступны только те объекты, у которых `is_demo=True`.

    Это полезно, когда необходимо:
    - ограничить демо-пользователя только демонстрационными сущностями;
    - исключить доступ к реальным данным через формы (например,
      при создании или редактировании объектов с внешними ключами).

    Использование:
    --------------
    1. Наследуйтесь от DemoModelForm в своих ModelForm-классах:

        class MyForm(DemoModelForm):
            class Meta:
                model = MyModel
                fields = ('field1', 'field2', ...)

    2. Передавайте `user` в kwargs при инициализации формы. Это
       делается автоматически, если используется DemoFormMixin во вьюхе:

        class MyCreateView(DemoFormMixin, CreateView):
            form_class = MyForm
            ...

    Примечания:
    ------------
    - Для корректной работы модели, на которые ссылаются поля формы,
      должны иметь поле `is_demo`.
    - Если поле связано с моделью без `is_demo`, то оно не фильтруется.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if getattr(user, 'is_demo', False):
            for field_name, field in self.fields.items():
                if isinstance(
                    field,
                    (forms.ModelChoiceField, forms.ModelMultipleChoiceField)
                ):
                    queryset = field.queryset
                    model = queryset.model
                    if hasattr(model, 'is_demo'):
                        self.fields[field_name].queryset = queryset.filter(
                            is_demo=True)
