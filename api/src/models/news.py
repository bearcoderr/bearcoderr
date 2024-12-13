import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from src.validators.compress_img import compress_img
from django.core.exceptions import ValidationError

class newsTag(models.Model):
    titleTag = models.CharField(verbose_name='Заголовок', max_length=500)
    slagTag = models.SlugField(verbose_name='Ссылка на тег', max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Генерируем `slug` только если его нет
        if not self.slagTag:
            base_slug = slugify(self.titleTag)
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

    def __str__(self):
        return self.titleTag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class newsCategory(models.Model):
    titleCategory = models.CharField(max_length=500, verbose_name='Заголовок')
    slagCategory = models.SlugField(max_length=500, verbose_name='Ссылка на категорию', blank=True, null=True)
    contentCategory = models.TextField(max_length=500, verbose_name='Контент категории')

    def save(self, *args, **kwargs):
        # Генерируем `slug` только если его нет
        if not self.slagCategory:
            base_slug = slugify(self.titleCategory)
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

    def __str__(self):
        return self.titleCategory

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class news(models.Model):
    imgnews = models.ImageField(upload_to='photos/news/', verbose_name='Главное изображение записи')
    dataNews = models.DateField(default=datetime.date.today, verbose_name='Дата публикации')
    countView = models.IntegerField(default=0, verbose_name='Сортировка для последних новостей')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время публикации')
    titlenews = models.CharField(max_length=500, verbose_name='Название статьи')
    slugnews = models.SlugField(max_length=200, unique=True, verbose_name='Заполняется автоматически', blank=True, null=True)
    contentnews = RichTextField(verbose_name='Контент Блог')
    tags = models.ManyToManyField('newsTag', blank=True, verbose_name='Теги статьи')
    category = models.ForeignKey('newsCategory', on_delete=models.SET_NULL, verbose_name='Категория', blank=True, null=True)

    ## Мини пост для соц сетей ##


    def __str__(self):
        return self.titlenews


    def is_published(self):
        """Проверка, что статья опубликована"""
        # Если поле published_at пустое, считаем статью опубликованной сразу
        if not self.published_at:
            return True
        # Если дата публикации заполнена, проверяем, не наступила ли она
        return self.published_at <= datetime.datetime.now()

    def save(self, *args, **kwargs):
        """Сохранение статьи"""
        # Генерация slug, если его нет
        if not self.slugnews:
            base_slug = slugify(self.titlenews)
            unique_slug = base_slug
            counter = 1

            while True:
                try:
                    self.slugnews = unique_slug
                    super().full_clean()  # Проверка уникальности через валидацию модели
                    break
                except ValidationError:
                    unique_slug = f"{base_slug}_{counter}"
                    counter += 1

        # Если дата и время публикации не указаны, ставим текущее время
        if not self.published_at:
            self.published_at = datetime.datetime.now()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Блог'


class Formsnews(models.Model):
    """Форма обратной связи"""

    nameComm = models.CharField(max_length=500, verbose_name='Имя')
    emailComm = models.EmailField(max_length=500, verbose_name='Email')
    textComm = models.TextField(verbose_name='Сообщение')
    time_create = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время отправки', auto_now_add=True)
    post = models.ForeignKey(news, on_delete=models.CASCADE, verbose_name='Новость')

    class Meta:
        verbose_name = 'Комментарий к Блог'
        verbose_name_plural = 'Комментарии к новостям'

    def __str__(self):
        return f'Вам письмо от {self.emailComm}'


