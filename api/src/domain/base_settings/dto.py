from dataclasses import dataclass
from typing import Optional
from django.core.files import File


@dataclass
class MenuSettingsDTO:
    nameLink: str
    link: str

@dataclass
class BaseSettingsDTO:
    titleHome: str
    imgHome: Optional[File] = None
    favSite: Optional[File] = None
    buttonHeader: str = ''
    copyText: str = ''
    admin_email: str = 'bearcoderr@gmail.com'
    menu_settings: list[MenuSettingsDTO] = None