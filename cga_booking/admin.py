from django.contrib import admin

from cga_booking.models import Hotel, Room, RoomReservation,\
    Attraction, Intro, InternalPhoto
# Register your models here.


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'address', 'website']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'belongs2']


@admin.register(RoomReservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'start_time', 'end_time', 'created_by']


@admin.register(Intro)
class IntroAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'content_flag', 'sequence', 'content_type', 'object_id']
    ordering = ('content_type', 'object_id', 'content_flag', 'sequence', 'id')


@admin.register(InternalPhoto)
class InternalPhotoAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'content_type', 'object_id', 'path']
    ordering = ('content_type', 'object_id', 'id')


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'name']
