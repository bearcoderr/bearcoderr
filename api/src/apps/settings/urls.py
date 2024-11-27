from django.urls import path
from .views import ViewHomes, ThanksView, sendEmail
from .render_resume import generate_pdf


urlpatterns = [
    path('', ViewHomes.as_view(), name='home'),
    path('forms/', ViewHomes.as_view(), name='forms'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('resume/', generate_pdf, name='resume'),
    path('send-email/', sendEmail.as_view(), name='send-email'),
]
