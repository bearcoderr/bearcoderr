import abc
from .dto import NewsDTO

class NewsRepositoryAbs(abc.ABC):

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