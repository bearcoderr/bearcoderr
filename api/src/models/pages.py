from django.db import models
from ckeditor.fields import RichTextField


class Pages(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    publication_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    id = models.AutoField(primary_key=True, db_index=True)

    class Meta:
        db_table = "custom_pages_table"
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return f"{self.title} ({self.slug})"
