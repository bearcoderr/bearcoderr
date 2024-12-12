from .repository_abs import NewsRepositoryAbs
from .dto import NewsDTO, CommentDTO, FeedDTO


class NewsService(NewsRepositoryAbs):
    def __init__(self, repository: NewsRepositoryAbs):
        self.repository = repository


    def get_news_list_category(self) -> list[NewsDTO]:
        return self.repository.get_news_list_category()

    def get_news_list_tag(self) -> list[NewsDTO]:
        return self.repository.get_news_list_tag()

    def get_news_list(self) -> list[NewsDTO]:
        return self.repository.get_news_list()

    def get_news_by_slug(self, slug: str) -> NewsDTO:
        return self.repository.get_news_by_slug(slug)

    def get_news_by_tag(self, tag: str) -> list[NewsDTO]:
        return self.repository.get_news_by_tag(tag)

    def get_news_by_category(self, category: str) -> list[NewsDTO]:
        return self.repository.get_news_by_category(category)

    def get_news_by_search(self, search: str) -> list[NewsDTO]:
        return self.repository.get_news_by_search(search)

    def get_popular_news(self) -> list[NewsDTO]:
        return self.repository.get_popular_news()

    def post_comment(self, comment: CommentDTO):
        return self.repository.post_comment(comment)

    def get_list_news_feed(self) -> list[FeedDTO]:
        return self.repository.get_list_news_feed()