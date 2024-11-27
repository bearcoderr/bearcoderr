from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from src.config import settings

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')

# Создаем объект Celery
app = Celery('api')

# Настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматический поиск задач по всему проекту
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')