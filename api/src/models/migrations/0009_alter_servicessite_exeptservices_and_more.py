# Generated by Django 5.1.3 on 2024-11-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_alter_experiencesettings_yearexperience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicessite',
            name='exeptServices',
            field=models.TextField(max_length=500, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='servicessite',
            name='titleServices',
            field=models.CharField(max_length=200, verbose_name='Название направления'),
        ),
    ]
