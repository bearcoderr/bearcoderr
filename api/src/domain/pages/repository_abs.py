from abc import ABC, abstractmethod
from src.domain.pages.dto import PagesDTO


class PageRepositoryAbs(ABC):
    @abstractmethod
    def get_all_pages(self) -> list[PagesDTO]:
        """Fetch all pages."""
        pass

    @abstractmethod
    def get_page_by_slug(self, slug: str) -> PagesDTO:
        """Fetch a single page by its slug."""
        pass
