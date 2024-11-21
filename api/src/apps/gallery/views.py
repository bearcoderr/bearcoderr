from django.views.generic.base import View
from src.models.gallery import GallerySite, Photo
from django.shortcuts import render, get_object_or_404


# Create your views here.


class GalleryViews(View):
    def get(self, request):
        gallerySet = GallerySite.objects.all()
        return render (request, 'gallery/gallery.html', {
            'gallerySet': gallerySet,
        })


class DetailsGalleryViews(View):
    def get(self, request, slug):
        galleryDetails = get_object_or_404(GallerySite, slugGallery=slug)
        galleryPhoto = Photo.objects.all()
        return render(request, 'gallery/gallery-details.html', {
            'galleryDetails': galleryDetails,
            'galleryPhoto': galleryPhoto,
        })