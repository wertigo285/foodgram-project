from django import template
from django.urls import reverse
register = template.Library()


@register.simple_tag(takes_context=True)
def set_activity_class(context, view_name):
    request_url = context['request'].path
    view_url = reverse(view_name)
    if request_url == view_url:
        return 'nav__item_active'
    return ''
