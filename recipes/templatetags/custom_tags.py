from django import template
register = template.Library()


@register.simple_tag
def is_favorite(recipe_favorite):
    if len(recipe_favorite):
        return 'icon-favorite_active'
    return ''
