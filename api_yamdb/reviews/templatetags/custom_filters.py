from django import template
from django.db.models import ManyToManyField
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def custom_getattr(obj, field_name):
    try:
        field = obj._meta.get_field(field_name)
        value = getattr(obj, field_name)

        if isinstance(field, ManyToManyField):
            return ", ".join(value.values_list('name', flat=True))

        return value
    except Exception:
        return ''


@register.filter
def field_verbose_name(obj, field_name):
    try:
        return obj._meta.get_field(field_name).verbose_name
    except Exception:
        return field_name


@register.filter
def rating_stars(value):
    """
    Преобразует рейтинг (0-10) в HTML с 5 звёздами.
    Пример: 7 → ★★★½☆☆
    """
    full_stars = int(value / 2)
    half_star = 1 if value % 2 == 1 else 0
    empty_stars = 5 - full_stars - half_star

    stars_html = []

    # Полные звёзды
    stars_html.extend(['<i class="fa-solid fa-star"></i>'] * full_stars)

    # Половина звезды
    if half_star:
        stars_html.append('<i class="fa-regular fa-star-half-stroke"></i>')

    # Пустые звёзды
    stars_html.extend(['<i class="fa-regular fa-star"></i>'] * empty_stars)

    return mark_safe(''.join(stars_html))
