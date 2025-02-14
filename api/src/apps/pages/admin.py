from django.contrib import admin
from src.models.pages import Pages


@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
