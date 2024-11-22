from django.views.generic.base import View
from django.shortcuts import render, redirect
from .repository import SettingsRepository
from src.domain.settings.services import SettingsServices


class ViewHomes(View):

    ## Выводим данные из БД ##
    def get(self, request):
        # Создаем экземпляр репозитория
        settings_repository = SettingsRepository()

        # Передаем репозиторий в сервис
        settings_services = SettingsServices(settings_repository=settings_repository)

        request.page_title = settings_services.get_settings().titleHome

        # Получаем настройки через сервис
        context = {
            'settings': settings_services.get_settings(),
        }

        # Рендерим шаблон с переданным контекстом
        return render(request, 'settings/index.html', context)