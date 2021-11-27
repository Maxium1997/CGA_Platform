from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from ocean_station.definitions import Region

register = template.Library()


@register.filter(name='readable_region')
def readable_region(region_code: int, language: int):
    region = list(Region.__members__.values())[region_code].value[language]
    return region
