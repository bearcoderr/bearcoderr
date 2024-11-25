import abc

from .dto import ServicesDTO


class ServicesRepositoryAbs(abc.ABC):
    @abc.abstractmethod
    def get_services(self) -> ServicesDTO:
        pass

    @abc.abstractmethod
    def get_services_list(self) -> list[ServicesDTO]:
        pass