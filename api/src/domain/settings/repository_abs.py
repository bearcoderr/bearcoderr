import abc
from .dto import SettingsDTO, FormSettingsDTO

class SettingsRepositoryAbs(abc.ABC):

    @abc.abstractmethod
    def get_settings(self) -> SettingsDTO:
        pass

    @abc.abstractmethod
    def post_fotms_settings(self, dto: FormSettingsDTO) -> FormSettingsDTO:
        """Сохраняет данные формы и возвращает DTO."""
        pass
