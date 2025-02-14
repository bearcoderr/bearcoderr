from django.urls import path
from .views import PageView

urlpatterns = [
    path('<slug:slug>/', PageView.as_view(), name='page'),
]
