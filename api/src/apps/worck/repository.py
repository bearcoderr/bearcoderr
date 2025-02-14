from src.domain.worck.services import WorkService
from src.domain.worck.dto import WorkCategoryDTO, WorkPreviewDTO, WorkDTO
from src.domain.worck.repository_abs import WorkRepositoryAbs
from src.models.worck import categoryWorck, WorckSite


class WorkRepository(WorkRepositoryAbs):
    def get_work_category_list(self) -> list[WorkCategoryDTO]:
        return categoryWorck.objects.all()

    def get_work_all(self) -> list[WorkPreviewDTO]:
        # Получаем все объекты WorckSite
        work_items = WorckSite.objects.all()

        # Преобразуем их в список DTO
        work_preview_dtos = [
            WorkPreviewDTO(
                id=work.id,
                imgWorck_thumb=work.imgWorck_thumb.url if work.imgWorck_thumb else "",
                titleWorck=work.titleWorck,
                exeptWorck=work.exeptWorck,
                categoryWorckInfo=" ".join([category.slugCategory for category in work.categoryWorckInfo.all()])
                # Передаем слаги
            )
            for work in work_items
        ]

        return work_preview_dtos

    def get_work_item(self, id: int) -> WorkDTO:
        work = WorckSite.objects.get(id=id)
        return WorkDTO(
            id=work.id,
            imgWorck_large=work.imgWorck_large.url if work.imgWorck_large else "",
            titleWorck=work.titleWorck,
            clientWorck=work.clientWorck,
            dateWorck=work.dateWorck,
            date_old_Worck=work.date_old_Worck,
            linkWorck=work.linkWorck,
            desk_title_Worck=work.desk_title_Worck,
            contentWorck=work.contentWorck,
            storyWorck=work.storyWorck,
            approachWorck=work.approachWorck,
            gallery_images = [img.gallery_img_Worck.url for img in work.gallery_images.all()],
            categoryWorckInfo=[category.slugCategory for category in work.categoryWorckInfo.all()],
        )
