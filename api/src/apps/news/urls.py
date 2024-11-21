from django.urls import path
from .views import (
    newsListView,
    newsDetailCategory,
    newsDetailTag,
    newsDetailView,
    SearchResultsView,
    FeedbackCreateView,
    contact_thanks_view,
    rss_feed
)

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', newsListView.as_view(), name='news_list'),
    path('rss/', rss_feed, name='rss_feed'),
    path('<slug:category_slug>/', newsDetailCategory.as_view(), name='news_category'),
    path('tag/<slug:tag_slug>/', newsDetailTag.as_view(), name='news_tag_detail'),
    path('<slug:category_slug>/<slug:slug>/', newsDetailView.as_view(), name='news_detail'),
    path('/feedback/', FeedbackCreateView, name='feedback'),
    path('/feedback/thanks/', contact_thanks_view, name='forms_home_thanks'),
]
