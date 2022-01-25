from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='mark')
def mark(obj, keyword):
    highlighted = str(obj).replace(keyword, '<mark>{}</mark>'.format(keyword))
    return mark_safe(highlighted)
