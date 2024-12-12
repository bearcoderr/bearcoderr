from typing import List
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from src.models.news import news, newsCategory, newsTag, Formsnews
from src.domain.news.repository_abs import NewsRepositoryAbs
from src.domain.news.dto import NewsDTO, NewsCategoryDTO, NewsTagDTO, CommentDTO, FeedDTO

class NewsRepository(NewsRepositoryAbs):


    def get_news_list_category(self) -> List[NewsCategoryDTO]:
        news_list = newsCategory.objects.all()
        return [
            NewsCategoryDTO(
                titleCategory=cat.titleCategory,
                slagCategory=cat.slagCategory,
                contentCategory=cat.contentCategory
            )
            for cat in news_list
        ]

    def get_news_list_tag(self) -> List[NewsTagDTO]:
        news_list = newsTag.objects.all()
        return [
            NewsTagDTO(
                titleTag=tag.titleTag,
                slagTag=tag.slagTag
            )
            for tag in news_list
        ]

    def get_popular_news(self) -> list[NewsDTO]:
        popular_news = news.objects.order_by('-countView')[:3]
        return [
            NewsDTO(
                post_id=new.id,
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
                dataNews=new.dataNews,
                slugnews=new.slugnews,
                contentnews=new.contentnews[:200],  # Ограничиваем текст
                tags=[
                    NewsTagDTO(
                        titleTag=tag.titleTag,
                        slagTag=tag.slagTag
                    ) for tag in new.tags.all()
                ],
                category=NewsCategoryDTO(
                    titleCategory=new.category.titleCategory,
                    slagCategory=new.category.slagCategory,
                    contentCategory=new.category.contentCategory
                ) if hasattr(new, 'category') else None
            )
            for new in popular_news
        ]

    def get_news_list(self) -> List[NewsDTO]:
        # Получаем текущую дату
        current_time = timezone.now()

        # Фильтруем новости по дате публикации и учитываем пустые значения
        news_list = news.objects.filter(
            Q(published_at__lte=current_time) | Q(published_at__isnull=True)
        ).prefetch_related('tags', 'category').order_by('-dataNews')

        return [
            NewsDTO(
                post_id=new.id,
                imgnews=new.imgnews.url if new.imgnews and hasattr(new.imgnews, 'url') else '',
                titlenews=new.titlenews,
                dataNews=new.dataNews,
                slugnews=new.slugnews,
                contentnews=new.contentnews,
                tags=[
                    NewsTagDTO(
                        titleTag=tag.titleTag,
                        slagTag=tag.slagTag
                    ) for tag in new.tags.all()
                ] if new.tags.exists() else [],
                category=NewsCategoryDTO(
                    titleCategory=new.category.titleCategory,
                    slagCategory=new.category.slagCategory,
                    contentCategory=new.category.contentCategory
                ) if new.category else None
            )
            for new in news_list
        ]

    def get_news_by_slug(self, slug: str) -> NewsDTO:
        new = news.objects.prefetch_related('tags', 'category').get(slugnews=slug)
        return NewsDTO(
            post_id=new.id,
            imgnews=new.imgnews.url if new.imgnews and hasattr(new.imgnews, 'url') else '',
            titlenews=new.titlenews,
            dataNews=new.dataNews,
            slugnews=new.slugnews,
            contentnews=new.contentnews,
            tags=[
                NewsTagDTO(
                    titleTag=tag.titleTag,
                    slagTag=tag.slagTag
                ) for tag in new.tags.all()
            ],
            category=NewsCategoryDTO(
                titleCategory=new.category.titleCategory,
                slagCategory=new.category.slagCategory,
                contentCategory=new.category.contentCategory
            ) if hasattr(new, 'category') else None
        )

    def get_news_by_tag(self, tag: str) -> list[NewsDTO]:
        news_list = news.objects.filter(tags__slagTag=tag).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                post_id=new.id,
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
                dataNews=new.dataNews,
                slugnews=new.slugnews,
                contentnews=new.contentnews,
                tags=[
                    NewsTagDTO(
                        titleTag=tag.titleTag,
                        slagTag=tag.slagTag
                    ) for tag in new.tags.all()
                ],
                category=NewsCategoryDTO(
                    titleCategory=new.category.titleCategory,
                    slagCategory=new.category.slagCategory,
                    contentCategory=new.category.contentCategory
                ) if hasattr(new, 'category') else None
            )
            for new in news_list
        ]

    def get_news_by_category(self, category_slug: str) -> list[NewsDTO]:
        category = newsCategory.objects.get(slagCategory=category_slug)
        news_list = news.objects.filter(category=category).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                post_id=new.id,
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
                dataNews=new.dataNews,
                slugnews=new.slugnews,
                contentnews=new.contentnews,
                tags=[
                    NewsTagDTO(
                        titleTag=tag.titleTag,
                        slagTag=tag.slagTag
                    ) for tag in new.tags.all()
                ],
                category=NewsCategoryDTO(
                    titleCategory=category.titleCategory,
                    slagCategory=category.slagCategory,
                    contentCategory=category.contentCategory
                ),
            )
            for new in news_list
        ]

    def get_news_by_search(self, search: str) -> list[NewsDTO]:
        news_list = news.objects.filter(titlenews__icontains=search).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                post_id=new.id,
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
                dataNews=new.dataNews,
                slugnews=new.slugnews,
                contentnews=new.contentnews,
                tags=[
                    NewsTagDTO(
                        titleTag=tag.titleTag,
                        slagTag=tag.slagTag
                    ) for tag in new.tags.all()
                ],
                category=[
                    NewsCategoryDTO(
                        titleCategory=cat.titleCategory,
                        slagCategory=cat.slagCategory
                    ) for cat in new.category.all()
                ],
            )
            for new in news_list
        ]

    def post_comment(self, comment: CommentDTO) -> CommentDTO:
        news_instance = get_object_or_404(news, pk=comment.post_id)

        # Создаем объект `Formsnews`, передавая экземпляр `news`
        form = Formsnews.objects.create(
            nameComm=comment.nameComm,
            emailComm=comment.emailComm,
            textComm=comment.textComm,
            post=news_instance
        )

        # Возвращаем DTO
        return CommentDTO(
            nameComm=form.nameComm,
            emailComm=form.emailComm,
            textComm=form.textComm,
            time_create=form.time_create,
            post_id=form.post.id
        )


    def get_list_news_feed(self) -> list[FeedDTO]:
        # Получаем текущую дату
        current_time = timezone.now()

        # Фильтруем новости по дате публикации и учитываем пустые значения
        news_feed_list = news.objects.filter(
            Q(published_at__lte=current_time) | Q(published_at__isnull=True)
        ).prefetch_related('tags', 'category').order_by('-dataNews')

        return [
            FeedDTO(
                imgnews=new.imgnews,
                titlenews=new.titlenews,
                slugnews=new.slugnews,
                contentnews=new.contentnews,
                text_twitter=new.text_twitter,
            )
            for new in news_feed_list
        ]