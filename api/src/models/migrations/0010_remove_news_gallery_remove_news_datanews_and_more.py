# Generated by Django 5.1.3 on 2024-11-25 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_alter_servicessite_exeptservices_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='gallery',
        ),
        migrations.RemoveField(
            model_name='news',
            name='datanews',
        ),
        migrations.AddField(
            model_name='news',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='formsnews',
            name='time_create',
            field=models.DateField(default=datetime.date, verbose_name='Дата публиации'),
        ),
        migrations.AlterField(
            model_name='newscategory',
            name='slagCategory',
            field=models.SlugField(blank=True, max_length=500, null=True, verbose_name='Ссылка на категорию'),
        ),
        migrations.AlterField(
            model_name='newstag',
            name='slagTag',
            field=models.SlugField(blank=True, max_length=200, null=True, verbose_name='Ссылка на тег'),
        ),
        migrations.DeleteModel(
            name='gallerynews',
        ),
        migrations.AddField(
            model_name='news',
            name='dataNews',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата публикации'),
        ),
    ]
