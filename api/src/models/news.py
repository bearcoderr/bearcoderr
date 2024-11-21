import datetime
from django.db import models
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone

TRANSLIT_DICT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
    'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
    'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
    'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
    'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
    'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
    'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
}

def custom_slugify(text):
    transliterated_text = ''.join(TRANSLIT_DICT.get(c, c) for c in text)
    sanitized_text = transliterated_text.replace("'", "").replace('"', "").replace(',', '').replace(';', '').replace(':', '')
    return sanitized_text.replace(' ', '-').lower()

class newsTag(models.Model):
    titleTag = models.CharField(verbose_name='Заголовок', max_length=500)
    slagTag = models.CharField(verbose_name='Ссылка на тег', max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slagTag:
            self.slagTag = custom_slugify(self.titleTag)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titleTag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'



class Formsnews(models.Model):
    """Форма обратной связи"""

    nameComm = models.CharField(max_length=500, verbose_name='Имя')
    emailComm = models.EmailField(max_length=500, verbose_name='Email')
    textComm = models.TextField(verbose_name='Сообщение')
    time_create = models.DateField(default=datetime.date.today, verbose_name='Дата публиации')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'Вам письмо от {self.emailComm}'


class gallerynews(models.Model):
    imgnews = models.ImageField(upload_to='photos/news/', verbose_name='Главное изображение записи')

    def __str__(self):
        return self.imgnews.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def save(self, *args, **kwargs):
        try:
            this = gallerynews.objects.get(id=self.id)
            if this.imgnews != self.imgnews:
                this.imgnews.delete(save=False)
                try:
                    new_image = self.compress_img(self.imgnews)
                    self.imgnews = new_image
                    super(gallerynews, self).save(*args, **kwargs)
                except ValueError:
                    super(gallerynews, self).save(*args, **kwargs)
            else:
                super(gallerynews, self).save(*args, **kwargs)
        except gallerynews.DoesNotExist:
            try:
                new_image = self.compress_img(self.imgnews)
                self.imgnews = new_image
                super(gallerynews, self).save(*args, **kwargs)
            except ValueError:
                super(gallerynews, self).save(*args, **kwargs)

    def compress_img(self, image, max_file_size=500000):
        im = Image.open(image)
        width, height = im.size

        # Желаемые размеры для обрезанного и сжатого изображения
        desired_width = 600
        desired_height = 500

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

        # Сжимаем изображение и уменьшаем качество до тех пор, пока размер файла не станет меньше указанного предела
        im_bytes = BytesIO()
        quality = 100
        im.save(im_bytes, format="WEBP", quality=quality)

        while im_bytes.tell() > max_file_size and quality > 10:
            im_bytes = BytesIO()
            quality -= 5
            im.save(im_bytes, format="WEBP", quality=quality)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + '.webp'
        new_image = File(image_content_file, name=name)
        return new_image


class newsCategory(models.Model):
    titleCategory = models.CharField(max_length=500, verbose_name='Заголовок')
    slagCategory = models.CharField(max_length=500, verbose_name='Ссылка на категорию', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slagCategory:
            self.slagCategory = custom_slugify(self.titleCategory)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titleCategory

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class news(models.Model):
    imgnews = models.ImageField(upload_to='photos/news/', verbose_name='Главное изображение записи')
    datanews = models.DateTimeField(default=timezone.now, verbose_name='Дата публиации')
    titlenews = models.CharField(max_length=500, verbose_name='Название статьи')
    slugnews = models.SlugField(max_length=200, unique=True, verbose_name='Заполняется автоматически', blank=True, null=True)
    contentnews = RichTextField(verbose_name='Контент новости')
    tags = models.ManyToManyField(newsTag, blank=True, verbose_name='Теги статьи')
    category = models.ManyToManyField(newsCategory, blank=True, verbose_name='Категории статьи')
    gallery = models.ManyToManyField(gallerynews, blank=True, verbose_name='Галерея фотографий')
    feetbicke = models.ForeignKey(Formsnews, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Отзыв')

    def save(self, *args, **kwargs):
        if not self.slugnews:
            self.slugnews = custom_slugify(self.titlenews)
        try:
            this = news.objects.get(id=self.id)
            if this.imgnews != self.imgnews:
                this.imgnews.delete(save=False)
                try:
                    new_image = self.compress_img(self.imgnews)
                    self.imgnews = new_image
                    super(news, self).save(*args, **kwargs)
                except ValueError:
                    super(news, self).save(*args, **kwargs)
            else:
                super(news, self).save(*args, **kwargs)
        except news.DoesNotExist:
            try:
                new_image = self.compress_img(self.imgnews)
                self.imgnews = new_image
                super(news, self).save(*args, **kwargs)
            except ValueError:
                super(news, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.titlenews

    def compress_img(self, image, max_file_size=500000):
        im = Image.open(image)
        width, height = im.size

        # Желаемые размеры для обрезанного и сжатого изображения
        desired_width = 1728
        desired_height = 672

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

        # Сжимаем изображение и уменьшаем качество до тех пор, пока размер файла не станет меньше указанного предела
        im_bytes = BytesIO()
        quality = 100
        im.save(im_bytes, format="WEBP", quality=quality)

        while im_bytes.tell() > max_file_size and quality > 10:
            im_bytes = BytesIO()
            quality -= 5
            im.save(im_bytes, format="WEBP", quality=quality)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + '.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    def get_absolute_url(self):
        category_slug = self.category.first().slagCategory if self.category.exists() else 'default-category'
        return reverse('news_detail', kwargs={'category_slug': category_slug, 'slug': self.slugnews})


