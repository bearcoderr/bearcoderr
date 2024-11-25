from django.views.generic.base import View
from django.shortcuts import render
from .repository import GalleryRepository
from src.domain.gallery.services import GalleryServices

class GalleryViews(View):
    def get(self, request):

        ##Сео настройки старницы##
        request.page_title = 'Путешествия Лехи бродяги'
        request.page_description = 'Это страница о моих путешествиях и открытиях. Я делюсь историями из поездок, случайными находками и приключениями. Если любишь нестандартные маршруты, тебе сюда!'

        gallery_repository = GalleryRepository()
        gallery_services = GalleryServices(gallery_repository)

        context = {
            'gallery': gallery_services.get_gallery_list()
        }

        return render(request, 'gallery/gallery.html', context)


class DetailsGalleryViews(View):
    def get(self, request, slug):

        gallery_repository = GalleryRepository()
        gallery_services = GalleryServices(gallery_repository)

        ##Сео настройки старницы##
        request.page_title = gallery_services.get_gallery(slug).titleGallery
        request.page_description = gallery_services.get_gallery(slug).contentGallery

        context = {
            'gallery': gallery_services.get_gallery(slug)
        }

        return render(request, 'gallery/gallery-details.html', context)