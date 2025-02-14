from django.views.generic.base import View
from django.shortcuts import render
from .repository import PagesRepository
from src.domain.pages.services import PagesServices


class PageView(View):
    def get(self, request, slug=None):
        pages_repository = PagesRepository()
        pages_services = PagesServices(pages_repository)

        # SEO настройки страницы
        page = pages_services.get_page_by_slug(slug or request.path)
        page_name = page.title  # Получаем название страницы
        request.page_title = page_name
        # Получаем срез в 250 символов с контента без символов HTML
        from django.utils.html import strip_tags
        request.page_description = strip_tags(page.content)[:250]

        context = {
            'page': pages_services.get_page_by_slug(slug or request.path)
        }
        return render(request, 'pages/page.html', context)
