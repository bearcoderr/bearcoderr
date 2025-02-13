from django.db import models
from ckeditor.fields import RichTextField
import datetime
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from src.validators.compress_img import compress_img

class GallerySite(models.Model):
    titleGallery = models.CharField(max_length=200, verbose_name='Название страницы с фотографиями', help_text='Не больше 200 символов')
    slugGallery = models.SlugField(unique=True, verbose_name="Ссылка")
    dataGallery = models.DateField(default=datetime.date.today, verbose_name='Дата поездки')
    contentGallery = RichTextField(verbose_name='Контент для галереи', blank=True, null=True)

    def __str__(self):
        return self.titleGallery

    def save(self, *args, **kwargs):
        # Генерируем `slug` только если его нет
        if not self.slugGallery:
            base_slug = slugify(self.titleGallery)
            unique_slug = base_slug
            counter = 1

            # Проверяем уникальность slug без запроса
            while True:
                try:
                    self.slugGallery = unique_slug
                    super().full_clean()  # Проверка уникальности через валидацию модели
                    break
                except ValidationError:
                    unique_slug = f"{base_slug}_{counter}"
                    counter += 1

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class Photo(models.Model):
    gallery = models.ForeignKey(GallerySite, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_photos')
    caption = models.CharField(max_length=200, blank=True)

    def image_preview(self):
        # Проверяем, если изображение существует
        if self.image:
            # Возвращаем HTML код для миниатюры изображения
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр'

    def save(self, *args, **kwargs):
        # Генерируем `caption` только если его нет

        if not self.caption and self.gallery:
            photo_count = Photo.objects.filter(gallery=self.gallery).count() + 1
            self.caption = f"{self.gallery.titleGallery} - Фото {photo_count}"
        super().save(*args, **kwargs)

        # Обработайте изображение только если оно было изменено или создано новое
        if self.image:
            compressed_image = compress_img(self.image)  # Вызываем импортированную функцию сжатия
            if compressed_image:
                self.image.save(compressed_image.name, compressed_image, save=False)

        # Сохраняем объект
        super().save(*args, **kwargs)

    def __str__(self):
        return self.caption



