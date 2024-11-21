from django.urls import path
from .views import GalleryViews, DetailsGalleryViews

urlpatterns = [
    path('', GalleryViews.as_view(), name='gallery_list'),
    path('<slug:slug>/', DetailsGalleryViews.as_view(), name='gallery_detail'),
    # Другие маршруты вашего приложения
]
