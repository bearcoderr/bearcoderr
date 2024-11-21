from django.urls import path
from .views import generate_pdf
from .views import FormsVievs, contact_thanks_view, ViewHomes


urlpatterns = [
    path('', ViewHomes.as_view(), name='home'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('forms/', FormsVievs, name='forms_home'),
    path('forms/thanks/', contact_thanks_view, name='forms_home_thanks'),
]
