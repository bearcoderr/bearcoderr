from django.contrib import admin
from django.utils.html import format_html
from src.models.worck import WorckSite, GalleryWorck, categoryWorck



@admin.register(GalleryWorck)
class GalleryWorckAdmin(admin.ModelAdmin):
    list_display = ('id', 'gallery_img_Worck')


@admin.register(categoryWorck)
class categoryWorckAdmin(admin.ModelAdmin):
    list_display = ('titleCategory', 'slugCategory')
    prepopulated_fields = {'slugCategory': ('titleCategory',)}


@admin.register(WorckSite)
class WorckSiteAdmin(admin.ModelAdmin):
    list_display = ('titleWorck', 'dateWorck', 'clientWorck', 'linkWorck', 'imgWorck_thumb_display')
    search_fields = ('titleWorck', 'clientWorck', 'exeptWorck')
    list_filter = ('dateWorck', 'categoryWorckInfo')
    filter_horizontal = ('categoryWorckInfo', 'gallery_images')

    # Метод для отображения миниатюры изображения в списке
    def imgWorck_thumb_display(self, obj):
        if obj.imgWorck_thumb:
            return format_html('<img src="{}" width="100" height="100" />', obj.imgWorck_thumb.url)
        return "Нет изображения"

    imgWorck_thumb_display.short_description = 'Миниатюра'

    # Настройка формы для редактирования изображения
    fieldsets = (
        (None, {
            'fields': (
            'titleWorck', 'exeptWorck', 'clientWorck', 'dateWorck', 'date_old_Worck', 'linkWorck', 'desk_title_Worck',
            'contentWorck', 'storyWorck', 'approachWorck', 'categoryWorckInfo', 'gallery_images')
        }),
        ('Изображения', {
            'fields': ('imgWorck_thumb', 'imgWorck_large')
        }),
    )

    # Форма с валидацией и использованием поля для изображений
    def save_model(self, request, obj, form, change):
        if change:
            # Если модель редактируется, обработаем изображения (миниатюра и большое изображение)
            obj.imgWorck_thumb = self.get_compressed_image(obj.imgWorck_thumb, 584, 500)
            obj.imgWorck_large = self.get_compressed_image(obj.imgWorck_large, 1028, 621)
        super().save_model(request, obj, form, change)

    # Метод для сжатия и преобразования изображения
    def get_compressed_image(self, image, width, height):
        if image:
            im = Image.open(image)
            width_original, height_original = im.size
            aspect_ratio = width_original / height_original
            new_height = int(width / aspect_ratio)
            im = im.resize((width, new_height))

            if new_height > height:
                x = 0
                y = (new_height - height) // 2
                area = (x, y, x + width, y + height)
                im = im.crop(area)

            im_bytes = BytesIO()
            im.save(im_bytes, format="WEBP", quality=100)
            image_content_file = ContentFile(im_bytes.getvalue())
            name = image.name.split('.')[0] + f'_{width}x{height}.webp'
            return File(image_content_file, name=name)
        return image
