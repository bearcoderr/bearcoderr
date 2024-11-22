import abc
from .dto import SettingsDTO

class SettingsRepositoryAbs(abc.ABC):

    @abc.abstractmethod
    def get_settings(self) -> SettingsDTO:
        pass
