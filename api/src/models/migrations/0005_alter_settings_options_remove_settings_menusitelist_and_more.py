# Generated by Django 5.1.3 on 2024-11-21 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_remove_gallerysite_exeptgallery_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Настройки сайта', 'verbose_name_plural': 'Настройки сайта'},
        ),
        migrations.RemoveField(
            model_name='settings',
            name='MenuSiteList',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='contactHome',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='experienceHome',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='numberlHome',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='skillsHome',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='socialHome',
        ),
        migrations.AddField(
            model_name='contactsettings',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiencesettings',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menusite',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='numbersettings',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skillssettings',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialsettings',
            name='settings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.settings'),
            preserve_default=False,
        ),
    ]
