from django.urls import path
from .views import ViewHomes


urlpatterns = [
    path('', ViewHomes.as_view(), name='home'),
]
