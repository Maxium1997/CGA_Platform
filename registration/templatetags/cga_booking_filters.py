from django import template
from django.utils.safestring import mark_safe

from cga_booking.definitions import ReservationStatus, ReservationUsages
from multi_relation.definitions import PaymentStatus

register = template.Library()


@register.filter(name='to_readable_room_usages')
def to_readable_room_usages(obj: int, language: int):
    return list(ReservationUsages.__members__.values())[obj-1].value[language]


@register.filter(name='to_readable_room_status')
def to_readable_room_status(obj: int, language: int):
    return list(ReservationStatus.__members__.values())[obj-1].value[language]


@register.filter(name='to_readable_room_payment_status')
def to_readable_room_payment_status(obj: int, language: int):
    return list(PaymentStatus.__members__.values())[obj-1].value[language]
