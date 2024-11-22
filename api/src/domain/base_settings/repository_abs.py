import abc
from .dto import BaseSettingsDTO

class BaseSettingsRepositoryAbs(abc.ABC):
    @abc.abstractmethod
    def get_settings(self) -> BaseSettingsDTO:
        pass