from django.db import models
from ckeditor.fields import RichTextField
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
# Create your models here.


class ServicesSite(models.Model):
    imgServices = models.ImageField(upload_to='media/services/', verbose_name='Главное изображение')
    titleServices = models.CharField(max_length=500, verbose_name='Название направления')
    exeptServices = models.CharField(max_length=500, verbose_name='Краткое описание')
    exeptServices = models.CharField(max_length=500, verbose_name='Краткое описание')
    contentServices = RichTextField(verbose_name='Контент услуги')


    def __str__(self):
        return self.titleServices

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


    def compress_img(self, image):
        im = Image.open(image)
        width, height = im.size

        # Желаемые размеры для обрезанного и сжатого изображения
        desired_width = 1028
        desired_height = 621

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
        name = image.name.split('.')[0] + '.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        try:
            this = ServicesSite.objects.get(id=self.id)
            if this.imgServices != self.imgServices:
                this.imgServices.delete(save=False)
                try:
                    new_image = self.compress_img(self.imgServices)
                    self.imgServices = new_image
                    super(ServicesSite, self).save(*args, **kwargs)
                except ValueError:
                    super(ServicesSite, self).save(*args, **kwargs)
            else:
                super(ServicesSite, self).save(*args, **kwargs)
        except ServicesSite.DoesNotExist:
            try:
                new_image = self.compress_img(self.imgServices)
                self.imgServices = new_image
                super(ServicesSite, self).save(*args, **kwargs)
            except ValueError:
                super(ServicesSite, self).save(*args, **kwargs)