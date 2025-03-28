from django import template

register = template.Library()


from django import template
from django.db.models import ManyToManyField

register = template.Library()

@register.filter
def custom_getattr(obj, field_name):
    try:
        field = obj._meta.get_field(field_name)
        value = getattr(obj, field_name)

        if isinstance(field, ManyToManyField):
            return ", ".join(value.values_list("name", flat=True))  # "name" — замените на нужное поле

        return value
    except Exception:
        return ""



@register.filter
def field_verbose_name(obj, field_name):
    try:
        return obj._meta.get_field(field_name).verbose_name
    except Exception as e:
        return field_name
