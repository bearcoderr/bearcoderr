from django.contrib import admin
from src.models.news import news, newsTag, newsCategory, Formsnews, gallerynews

@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    list_display = ('titlenews', 'slugnews', 'datanews')  # Замените 'status' на правильное имя поля

@admin.register(newsTag)
class newsTagAdmin(admin.ModelAdmin):
    pass

@admin.register(newsCategory)
class newsCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(gallerynews)
class gallerynewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Formsnews)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('nameComm', 'emailComm', 'textComm', 'time_create')

