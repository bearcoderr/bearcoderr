from django.urls import path
from .views import NewsView, NewsDetailsView


urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('<str:category_slug>/<str:news_slug>/', NewsDetailsView.as_view(), name='news_detail'),
]