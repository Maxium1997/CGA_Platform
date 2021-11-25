from django.contrib import admin

from ocean_station.models import Station, TaggedAttraction, Content
# Register your models here.


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'manager', 'region', 'fans_page_url']


@admin.register(TaggedAttraction)
class TaggedAttractionAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'name']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'content_flag', 'sequence', 'content_type', 'object_id']
    ordering = ('content_type', 'object_id', 'content_flag', 'sequence', 'id')
