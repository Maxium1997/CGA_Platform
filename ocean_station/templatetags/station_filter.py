from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from ocean_station.definitions import Region, ContentFlag

register = template.Library()


@register.filter(name='readable_region')
def readable_region(region_code: int, language: int):
    region = list(Region.__members__.values())[region_code].value[language]
    return region


@register.filter(name='readable_content_flag')
def readable_content_flag(content_code: int, language: int):
    content_flag = list(ContentFlag.__members__.values())[content_code-1].value[language]
    return content_flag
