from .repository_abs import ServicesRepositoryAbs
from .dto import ServicesDTO


class ServicesServices:
    def __init__(self, repository: ServicesRepositoryAbs):
        self.repository = repository

    def get_services(self) -> ServicesDTO:
        return self.repository.get_services()

    def get_services_list(self) -> list[ServicesDTO]:
        return self.repository.get_services_list()