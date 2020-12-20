from django import template
from django.urls import reverse


from recipes.models import ShoppingList 

register = template.Library()


@register.simple_tag(takes_context=True)
def set_activity_class(context, *args):
    request = context['request']
    current_view_name = request.resolver_match.view_name
    if current_view_name in args:
        return 'nav__item_active'
    return ''


@register.simple_tag(takes_context=True)
def shopping_list_counter(context, *args):
    user = context['request'].user
    counter = len(ShoppingList.objects.filter(user=user))

    return counter