from django.db import models
from ckeditor.fields import RichTextField
from src.validators.compress_img import compress_img
# Create your models here.


class ServicesSite(models.Model):
    imgServices = models.ImageField(upload_to='media/services/', verbose_name='Главное изображение')
    titleServices = models.CharField(max_length=200, verbose_name='Название направления')
    exeptServices = models.TextField(max_length=500, verbose_name='Краткое описание')
    contentServices = RichTextField(verbose_name='Контент услуги')


    def __str__(self):
        return self.titleServices

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def save(self, *args, **kwargs):
        if self.imgServices:
            new_image = compress_img(self.imgServices, desired_width=1028, desired_height=621)
            self.imgServices = new_image
        super().save(*args, **kwargs)
