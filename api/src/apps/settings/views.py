from django.views.generic.base import View
from django.shortcuts import render
from .repository import SettingsRepository
from src.domain.settings.services import SettingsServices
from src.domain.services.services import ServicesServices
from src.apps.services.repository import ServicesRepository
# Подключаем Блог
from src.domain.news.services import NewsService
from src.apps.news.repository import NewsRepository



class ViewHomes(View):

    ## Выводим данные из БД ##
    def get(self, request):
        # Создаем экземпляр репозитория
        settings_repository = SettingsRepository()

        services_repository = ServicesRepository()
        services_services = ServicesServices(services_repository)

        # Передаем репозиторий в сервис
        settings_services = SettingsServices(settings_repository=settings_repository)
        request.page_title = settings_services.get_settings().titleHome

        news_repository = NewsRepository()
        news_services = NewsService(news_repository)

        # Получаем настройки через сервис
        context = {
            'settings': settings_services.get_settings(),
            'services': services_services.get_services_list(),
            'news_list': news_services.get_news_list()[:3]
        }

        # Рендерим шаблон с переданным контекстом
        return render(request, 'settings/index.html', context)
