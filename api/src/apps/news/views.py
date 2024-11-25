from django.views.generic.base import View
from django.shortcuts import render
from .repository import NewsRepository
from src.domain.news.services import NewsService
from django.http import Http404

class NewsView(View):
    def get(self, request):

        news_repository = NewsRepository()
        news_services = NewsService(news_repository)

        ##Сео настройки старницы##
        request.page_title = 'Статьи про программирование и прочее'
        request.page_description = 'Это страница с новостями о программировании и прочих интересных вещей'

        context = {
            'news_list': news_services.get_news_list()
        }

        return render(request, 'news/blog.html', context)

class NewsDetailsView(View):
    def get(self, request, category_slug, slug):
        news_repository = NewsRepository()
        news_service = NewsService(news_repository)

        # Получаем новость
        news = news_service.get_news_by_slug(slug)

        # Берем последнюю категорию как основную
        main_category = news.category.first()

        # SEO настройки страницы
        request.page_title = news.titlenews
        request.page_description = news.contentnews[:160]

        context = {
            'news': news_service.get_news_by_slug(slug),
            'main_category': main_category
        }

        return render(request, 'news/blog-details.html', context)
