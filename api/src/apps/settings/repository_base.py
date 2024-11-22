from src.models.settings import Settings, MenuSite
from src.domain.base_settings.dto import BaseSettingsDTO, MenuSettingsDTO
from src.domain.base_settings.repository_abs import BaseSettingsRepositoryAbs

class BaseSettingsRepository(BaseSettingsRepositoryAbs):
    def get_settings(self) -> BaseSettingsDTO:
        settings = Settings.objects.first()
        return BaseSettingsDTO(
            titleHome=settings.titleHome,
            imgHome=settings.imgHome,
            favSite=settings.favSite,
            buttonHeader=settings.buttonHeader,
            copyText=settings.copyText,
            admin_email=settings.admin_email,
            menu_settings=[MenuSettingsDTO(nameLink=menu.nameLink, link=menu.link) for menu in MenuSite.objects.all()]
        )