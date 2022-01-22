from django.contrib import admin

from cga_case.models import CaseCategory, CaseSection, Case

# Register your models here.


@admin.register(CaseCategory)
class CaseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CaseSection)
class CaseSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_part_of', 'name']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'title']
