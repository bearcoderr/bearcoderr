from django.urls import path
from .views import NewsView, NewsDetailsView, NewsCategoryView, NewsFeed


urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('feed/', NewsFeed(), name='news_feed'),
    path('<str:category_slug>/', NewsCategoryView.as_view(), name='news_category_list'),
    path('<str:category_slug>/<str:news_slug>/', NewsDetailsView.as_view(), name='news_detail'),

]