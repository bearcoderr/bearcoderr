import abc
from .dto import NewsDTO, CommentDTO

class NewsRepositoryAbs(abc.ABC):

    @abc.abstractmethod
    def get_news_list_category(self) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_news_list_tag(self) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_news_list(self) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_news_by_slug(self, slug: str) -> NewsDTO:
        pass

    @abc.abstractmethod
    def get_news_by_tag(self, tag: str) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_news_by_category(self, category: str) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_news_by_search(self, search: str) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def get_popular_news(self) -> list[NewsDTO]:
        pass

    @abc.abstractmethod
    def post_comment(self, comment: CommentDTO) -> CommentDTO:
        pass