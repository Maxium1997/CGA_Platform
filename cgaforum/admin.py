from django.contrib import admin


from cgaforum.models import Category, SubCategory, Topic
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    ordering = ['id']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'f']
    ordering = ['f', 'id']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'published_time', 'created_by']
