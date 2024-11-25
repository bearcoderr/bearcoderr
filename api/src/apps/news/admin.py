from django.contrib import admin
from src.models.news import news, newsCategory, newsTag, Formsnews

# Register your models here.
@admin.register(newsCategory)
class newsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slagCategory': ('titleCategory',)}
    list_display = ['titleCategory']

@admin.register(newsTag)
class newsTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slagTag': ('titleTag',)}
    list_display = ['titleTag']

@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugnews': ('titlenews',)}
    list_display = ['titlenews', 'dataNews']


@admin.register(Formsnews)
class FormsnewsAdmin(admin.ModelAdmin):
    list_display = ['nameComm', 'emailComm', 'time_create', 'post']

