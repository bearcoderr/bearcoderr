from django.core.mail import send_mail
from django.conf import settings

def send_email(to_email):
    subject = "Тема письма"
    message = "Текст письма"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Отправка письма через SMTP сервер
    send_mail(subject, message, from_email, [to_email])
