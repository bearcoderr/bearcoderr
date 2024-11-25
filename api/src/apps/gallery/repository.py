from src.models.gallery import GallerySite, Photo
from src.domain.gallery.dto import PhotoDTO, GalleryDTO
from src.domain.gallery.repository_abs import GalleryRepositoryAbs

class GalleryRepository(GalleryRepositoryAbs):
    def get_gallery(self, slug: str) -> GalleryDTO:
        gallery = GallerySite.objects.get(slugGallery=slug)
        return GalleryDTO(
            titleGallery=gallery.titleGallery,
            slugGallery=gallery.slugGallery,
            dataGallery=gallery.dataGallery,
            contentGallery=gallery.contentGallery,
            photos=[PhotoDTO(caption=photo.caption, image_url=photo.image.url) for photo in gallery.photos.all()],
        )

    def get_gallery_list(self) -> list[GalleryDTO]:
        galleries = GallerySite.objects.all()
        return [GalleryDTO(
            titleGallery=gallery.titleGallery,
            slugGallery=gallery.slugGallery,
            dataGallery=gallery.dataGallery,
            contentGallery=gallery.contentGallery,
            photos=[PhotoDTO(caption=photo.caption, image_url=photo.image.url) for photo in gallery.photos.all()],
        ) for gallery in galleries]