from dataclasses import dataclass
from typing import Optional
from django.core.files import File


@dataclass
class ServicesDTO:
    titleServices: str = "Default Service Title"
    contentServices: str = "Default Content for Services"
    exeptServices: str = "Default Exceptions for Services"
    imgServices: Optional[File] = None