from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
import datetime
from ckeditor.fields import RichTextField

# Upload function for gallery images
def upload_gallery_to(instance, filename):
    return f'photos/media/gallery/{filename}'

# Upload function for work images
def upload_worck_to(instance, filename):
    return f'photos/worck/{filename}'

# Model for gallery images
class GalleryWorck(models.Model):
    gallery_img_Worck = models.ImageField(upload_to=upload_gallery_to, verbose_name='Добавить фото')

    def __str__(self):
        return f'Изображение для {self.id}'

    class Meta:
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Изображения галереи'

class categoryWorck(models.Model):
    titleCategory = models.CharField(max_length=500, verbose_name='Название категории')
    slugCategory = models.CharField(max_length=500, verbose_name='Ссылка на категорию')

    def __str__(self):
        return self.titleCategory

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Model for work site
class WorckSite(models.Model):
    imgWorck_thumb = models.ImageField(upload_to=upload_worck_to, verbose_name='Миниатюра изображения')
    imgWorck_large = models.ImageField(upload_to=upload_worck_to, verbose_name='Большое изображение')
    titleWorck = models.CharField(max_length=500, verbose_name='Заголовок')
    exeptWorck = models.TextField(max_length=500, verbose_name='Краткое описание')
    clientWorck = models.CharField(max_length=500, verbose_name='Клиент', blank=True)
    dateWorck = models.DateField(default=datetime.date.today, verbose_name='Дата старта работы')
    date_old_Worck = models.DateField(default=datetime.date.today, verbose_name='Дата окончания работы')
    linkWorck = models.CharField(max_length=500, verbose_name='Ссылка', blank=True)
    desk_title_Worck = models.CharField(max_length=500, verbose_name='Заголовок блока описания')
    contentWorck = RichTextField(verbose_name='Контент работы')
    storyWorck = models.TextField(verbose_name='История работы', blank=True)
    approachWorck = models.TextField(verbose_name='Описание что было сделано', blank=True)
    gallery_images = models.ManyToManyField(GalleryWorck, related_name='related_works', blank=True)
    categoryWorckInfo = models.ManyToManyField(categoryWorck, verbose_name='Категория для работы', blank=True)

    def __str__(self):
        return self.titleWorck

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def compress_img(self, image, desired_width, desired_height):
        im = Image.open(image)
        width, height = im.size

        # Рассчитываем соотношение сторон текущего изображения
        aspect_ratio = width / height

        # Вычисляем новую высоту, сохраняя пропорции
        new_height = int(desired_width / aspect_ratio)

        # Масштабируем изображение до новых размеров
        im = im.resize((desired_width, new_height))

        # Обрезаем изображение, если необходимо
        if new_height > desired_height:
            x = 0
            y = (new_height - desired_height) // 2
            area = (x, y, x + desired_width, y + desired_height)
            im = im.crop(area)

        # Сохраняем изображение в формате WEBP
        im_bytes = BytesIO()
        im.save(im_bytes, format="WEBP", quality=100)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + f'_{desired_width}x{desired_height}.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект чтобы получить его ID
        super(WorckSite, self).save(*args, **kwargs)

        # Обработайте изображение только если оно было изменено или создано новое
        if 'imgWorck' in self.__dict__:
            try:
                # Создайте миниатюру и большое изображение
                thumb_image = self.compress_img(self.imgWorck, 584, 500)
                large_image = self.compress_img(self.imgWorck, 1028, 621)

                # Обновите поля изображения
                self.imgWorck_thumb.save(thumb_image.name, thumb_image, save=False)
                self.imgWorck_large.save(large_image.name, large_image, save=False)

                # Сохраните изменения
                super(WorckSite, self).save(update_fields=['imgWorck_thumb', 'imgWorck_large'])
            except Exception as e:
                print(f"Ошибка при обработке изображения: {e}")

