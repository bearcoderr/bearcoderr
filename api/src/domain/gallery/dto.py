from dataclasses import dataclass
from typing import List

@dataclass
class PhotoDTO:
    caption: str
    image_url: str

@dataclass
class GalleryDTO:
    titleGallery: str
    slugGallery: str
    dataGallery: str
    contentGallery: str
    photos: List[PhotoDTO]

