from .repository_abs import GalleryRepositoryAbs
from .dto import GalleryDTO


class GalleryServices(GalleryRepositoryAbs):
    def __init__(self, repository: GalleryRepositoryAbs):
        self.repository = repository

    def get_gallery(self, slug: str) -> GalleryDTO:
        return self.repository.get_gallery(slug)

    def get_gallery_list(self) -> list[GalleryDTO]:
        return self.repository.get_gallery_list()