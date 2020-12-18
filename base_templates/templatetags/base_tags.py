from django import template
from django.urls import reverse
register = template.Library()


@register.simple_tag(takes_context=True)
def set_activity_class(context, *args):
    request = context['request']
    current_view_name = request.resolver_match.view_name
    if current_view_name in args:
        return 'nav__item_active'
    return ''
