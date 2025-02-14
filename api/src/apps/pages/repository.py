from src.models.pages import Pages
from src.domain.pages.repository_abs import PageRepositoryAbs
from src.domain.pages.dto import PagesDTO

class PagesRepository(PageRepositoryAbs):
    def get_all_pages(self) -> list[PagesDTO]:
        pages = Pages.objects.all()
        return [PagesDTO(
            id=page.id,
            slug=page.slug,
            title=page.title,
            content=page.content,
            publication_date=page.publication_date,
            last_updated=page.last_updated
        ) for page in pages]

    def get_page_by_slug(self, slug: str) -> PagesDTO:
        page = Pages.objects.get(slug=slug)
        return PagesDTO(
            id=page.id,
            slug=page.slug,
            title=page.title,
            content=page.content,
            publication_date=page.publication_date,
            last_updated=page.last_updated
        )
