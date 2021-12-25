from django.contrib import admin

from cga_booking.models import Hotel, Room, Attraction, Intro, InternalPhoto
# Register your models here.


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'address', 'website']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'belongs2']


@admin.register(InternalPhoto)
class InternalPhotoAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'content_type', 'object_id', 'path']
    ordering = ('content_type', 'object_id', 'id')
