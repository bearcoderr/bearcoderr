from src.models.services import ServicesSite
from src.domain.services.repository_abs import ServicesRepositoryAbs
from src.domain.services.dto import ServicesDTO


class ServicesRepository(ServicesRepositoryAbs):
    def get_services_list(self) -> list[ServicesDTO]:
        return ServicesSite.objects.all()

    def get_services(self) -> ServicesDTO:
        return ServicesSite.objects.first()