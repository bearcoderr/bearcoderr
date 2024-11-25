from dataclasses import dataclass
from typing import Optional
from django.core.files import File


@dataclass
class ServicesDTO:
    titleServices: str
    contentServices: str
    exeptServices: str
    imgServices: Optional[File] = None