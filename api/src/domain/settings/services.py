from .repository_abs import SettingsRepositoryAbs
from .dto import SettingsDTO, FormSettingsDTO


class SettingsServices:
    def __init__(self, settings_repository: SettingsRepositoryAbs):
        self.__settings_repository = settings_repository

    def get_settings(self) -> SettingsDTO:
        return self.__settings_repository.get_settings()

    def post_fotms_settings(self, dto: FormSettingsDTO) -> FormSettingsDTO:
        return self.__settings_repository.post_fotms_settings(dto)

