from src.models.news import news, newsCategory, newsTag
from src.domain.news.repository_abs import NewsRepositoryAbs
from src.domain.news.dto import NewsDTO, NewsCategoryDTO, NewsTagDTO

class NewsRepository(NewsRepositoryAbs):
    def get_news_list(self) -> list[NewsDTO]:
        news_list = news.objects.prefetch_related('tags', 'category').all()
        return [
            NewsDTO(
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
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
                        slagCategory=cat.slagCategory,
                    ) for cat in new.category.all()
                ],
            )
            for new in news_list
        ]

    def get_news_by_slug(self, slug: str) -> NewsDTO:
        new = news.objects.prefetch_related('tags', 'category').get(slugnews=slug)
        # Допустим, берем первую категорию как основную
        main_category = new.category.first()  # Получаем первую категорию, если она есть
        return NewsDTO(
            imgnews=new.imgnews.url if new.imgnews else '',
            titlenews=new.titlenews,
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
                    slagCategory=cat.slagCategory  # Только одно поле slug
                ) for cat in new.category.all()
            ],
        )

    def get_news_by_tag(self, tag: str) -> list[NewsDTO]:
        news_list = news.objects.filter(tags__slagTag=tag).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
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

    def get_news_by_category(self, category: str) -> list[NewsDTO]:
        news_list = news.objects.filter(category__slagCategory=category).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
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

    def get_news_by_search(self, search: str) -> list[NewsDTO]:
        news_list = news.objects.filter(titlenews__icontains=search).prefetch_related('tags', 'category')
        return [
            NewsDTO(
                imgnews=new.imgnews.url if new.imgnews else '',
                titlenews=new.titlenews,
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
