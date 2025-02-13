from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .repository import NewsRepository

from .forms import FeedbackCreateForm
from src.domain.news.dto import CommentDTO
from django.utils.timezone import now

from src.domain.news.services import NewsService
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed


class NewsView(View):
    def get(self, request):
        news_repository = NewsRepository()
        news_services = NewsService(news_repository)

        # Получаем все опубликованные новости
        news_list = news_services.get_news_list()

        # Пагинация
        paginator = Paginator(news_list, 10)  # 10 новостей на страницу
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.get_page(1)

        # SEO настройки страницы
        request.page_title = 'Статьи про программирование и прочее'
        request.page_description = 'Это страница с новостями о программировании и прочих интересных вещах'

        context = {
            'news_list': page_obj,  # Объект страницы
            'categories': news_services.get_news_list_category() or [],
            'tags': news_services.get_news_list_tag() or [],
            'popular_news': news_services.get_popular_news() or [],
        }

        return render(request, 'news/blog.html', context)


class NewsCategoryView(View):
    def get(self, request, category_slug):
        news_repository = NewsRepository()
        news_service = NewsService(news_repository)

        # Получаем новости по категории
        news_list = news_service.get_news_by_category(category_slug)

        if not news_list:
            raise Http404("Категория не найдена или пустая")

        # SEO настройки страницы
        category = news_list[0].category
        request.page_title = getattr(category, 'titleCategory', 'Категория отсутствует')
        request.page_description = getattr(category, 'contentCategory', 'Описание отсутствует')

        context = {
            'news_list': news_list,
            'categories': news_service.get_news_list_category() or [],
            'tags': news_service.get_news_list_tag() or [],
            'popular_news': news_service.get_popular_news() or [],
        }
        return render(request, 'news/blog.html', context)


class NewsDetailsView(View):
    def get(self, request, category_slug, news_slug):
        news_repository = NewsRepository()
        news_service = NewsService(news_repository)

        # Получаем новость
        news = news_service.get_news_by_slug(news_slug)

        # SEO настройки страницы
        request.page_title = getattr(news, 'titlenews', 'Новость отсутствует')
        request.page_description = getattr(news, 'contentnews', '')[:200]

        form = FeedbackCreateForm()

        context = {
            'news_info': news,
            'form': form
        }

        return render(request, 'news/blog-details.html', context)

    def post(self, request, category_slug, news_slug):
        news_repository = NewsRepository()
        news_service = NewsService(news_repository)

        # Получаем новость
        news = news_service.get_news_by_slug(news_slug)

        # SEO настройки страницы
        request.page_title = getattr(news, 'titlenews', 'Новость отсутствует')
        request.page_description = getattr(news, 'contentnews', '')[:200]

        form = FeedbackCreateForm(request.POST)

        if form.is_valid():
            # Преобразуем данные формы в DTO
            form_dto = CommentDTO(
                nameComm=form.cleaned_data['nameComm'],
                emailComm=form.cleaned_data['emailComm'],
                textComm=form.cleaned_data['textComm'],
                time_create=now(),
                post_id=news.post_id
            )

            # Создаем репозиторий и сервис для обработки формы
            news_repository = NewsRepository()
            news_service = NewsService(news_repository)

            # Сохраняем данные через сервис
            news_service.post_comment(form_dto)

            # Уведомление об успешной отправке
            request.session['message'] = 'Ваша заявка успешно отправлена!'

            # Перенаправляем на главную страницу или другую страницу
            return redirect('thanks')  # Или другой путь

        # Если форма не валидна, возвращаем ошибку и повторно рендерим страницу
        news_repository = NewsRepository()
        news_service = NewsService(news_repository)

        form = FeedbackCreateForm()

        news = news_service.get_news_by_slug(news_slug)


        context = {
            'news_info': news,
            'form': form
        }

        return render(request, 'news/blog-details.html', context)




class YandexZenFeedGenerator(Rss201rev2Feed):
    """RSS генератор для Яндекс.Дзена"""
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement("pdalink", item['pdalink'])
        handler.addQuickElement("media:rating", item['media_rating'])
        handler.addQuickElement("content:encoded", item['content'])


class NewsFeed(Feed):
    feed_type = YandexZenFeedGenerator
    title = "Опытный Backend-разработчик Алексей Ачкасов"
    link = 'https://bearcoder.ru/'  # Используем настройку из settings
    description = "RSS-лента содержит последние новости о разработке, программировании и IT-трендах. Обновления включают статьи, обзоры и полезный контент для разработчиков и специалистов в сфере технологий."

    get_list_news_feed = NewsRepository()
    news_services = NewsService(get_list_news_feed)

    def items(self):
        # Возвращаем только те статьи, у которых есть текст в блоке text_twitter
        return [item for item in self.news_services.get_list_news_feed() if item.text_twitter]

    def item_title(self, item):
        return item.titlenews

    def item_description(self, item):
        return item.text_twitter[:250]  # Краткий анонс новости

    def item_link(self, item):
        return f"http://localhost:8001/news/{item.slugnews}/" if hasattr(item, 'slugnews') and item.slugnews else 'http://localhost:8001/'

    def item_extra_kwargs(self, item):
        return {
            'pdalink': f"http://localhost:8001/news/{item.slugnews}/" if hasattr(item, 'slugnews') and item.slugnews else 'http://localhost:8001/',
            'media_rating': "nonadult",
            'content': f"<![CDATA[{item.contentnews}]]>" if hasattr(item, 'contentnews') and item.contentnews else "",
        }
