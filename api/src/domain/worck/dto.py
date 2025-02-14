from dataclasses import dataclass


@dataclass
class WorkCategoryDTO:
    slug: str
    name: str

@dataclass
class WorkPreviewDTO:
    id: int
    imgWorck_thumb: str
    titleWorck: str
    exeptWorck: str
    categoryWorckInfo: str


@dataclass
class WorkDTO:
    id: int
    imgWorck_large: str
    titleWorck: str
    clientWorck: str
    dateWorck: str
    date_old_Worck: str
    linkWorck: str
    desk_title_Worck: str
    contentWorck: str
    storyWorck: str
    approachWorck: str
    gallery_images: list
    categoryWorckInfo: str
