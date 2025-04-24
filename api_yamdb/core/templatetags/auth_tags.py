from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def user_object_url(context, obj):
    request = context['request']
    if hasattr(obj, 'get_admin_url') and (
        request.user.is_admin
        or request.user.is_superuser
        or request.user.role == "superuser"):
        return obj.get_admin_url()
    return obj.get_absolute_url()