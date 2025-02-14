from .repository_abs import WorkRepositoryAbs
from .dto import WorkCategoryDTO

class WorkService:
    def __init__(self, work_repository: WorkRepositoryAbs):
        self.work_repository = work_repository

    def get_work_category_list(self) -> list[WorkCategoryDTO]:
        return self.work_repository.get_work_category_list()

    def get_work_all(self) -> list[WorkCategoryDTO]:
        return self.work_repository.get_work_all()

    def get_work_item(self, work_id: int) -> WorkCategoryDTO:
        return self.work_repository.get_work_item(work_id)