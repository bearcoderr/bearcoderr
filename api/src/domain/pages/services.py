from src.domain.pages.repository_abs import PageRepositoryAbs
from src.domain.pages.dto import PagesDTO


class PagesServices:
    def __init__(self, repository: PageRepositoryAbs):
        self.repository = repository

    def get_all_pages(self) -> list[PagesDTO]:
        """
        Fetch all pages.
        :return: A list of PagesDTO objects.
        """
        return self.repository.get_all_pages()

    def get_page_by_slug(self, slug: str) -> PagesDTO:
        """
        Fetch a single page by its slug.
        :param slug: The slug of the page.
        :return: A PagesDTO object representing the page.
        """
        return self.repository.get_page_by_slug(slug)
