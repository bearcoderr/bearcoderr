import abc

from .dto import GalleryDTO


class GalleryRepositoryAbs(abc.ABC):

    @abc.abstractmethod
    def get_gallery(self) -> GalleryDTO:
        pass

    @abc.abstractmethod
    def get_gallery_list(self) -> list[GalleryDTO]:
        pass