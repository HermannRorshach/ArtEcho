from django import forms


class DemoModelForm(forms.ModelForm):
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
