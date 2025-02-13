from django.contrib import admin
from src.models.gallery import GallerySite, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3
    fields = ['image', 'caption']
    readonly_fields = ['image_preview']  # Делаем поле 'image_preview' доступным только для чтения

    # Для редактирования полей изображения и подписи
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:  # Если объект уже существует, не даем редактировать миниатюру
            return ['image_preview', 'caption', 'image']
        return fields

@admin.register(GallerySite)
class GallerySiteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugGallery': ('titleGallery',)}
    inlines = [PhotoInline]

    list_display = ['titleGallery', 'dataGallery']
    actions = ['duplicate_records']

    def duplicate_records(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Сбросить первичный ключ, чтобы создать новую запись
            obj.id = None  # Очистить id, если это поле не автоинкрементное
            obj.save()

    duplicate_records.short_description = "Дублировать записи"

