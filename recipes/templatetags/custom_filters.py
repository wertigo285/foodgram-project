from django import template
register = template.Library()



@register.filter
def test(b):
    a = 1
    return ''