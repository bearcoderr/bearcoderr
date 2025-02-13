from .repository_abs import BaseSettingsRepositoryAbs
from .dto import BaseSettingsDTO


class BaseSettingsService:
    def __init__(self, repository: BaseSettingsRepositoryAbs):
        self.repository = repository

    def get_settings(self) -> BaseSettingsDTO:
        return self.repository.get_settings()