import abc
from .dto import WorkCategoryDTO


class WorkRepositoryAbs(abc.ABC):
    @abc.abstractmethod
    def get_work_category_list(self) -> list[WorkCategoryDTO]:
        pass

    def get_work_all(self) -> list[WorkCategoryDTO]:
        pass

    def get_work_item(self, work_id: int) -> WorkCategoryDTO:
        pass