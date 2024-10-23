from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from .tokens import email_confirmation_token


def send_confirmation_email(request, user):
    token = email_confirmation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Генерация URL подтверждения
    confirm_url = reverse('confirm_email', kwargs={
        'uidb64': uid,
        'token': token,
    })

    # Использование build_absolute_uri для получения полного URL
    link = request.build_absolute_uri(confirm_url)

    # Заголовок и сообщение
    subject = 'Подтверждение электронной почты'
    message = f"Привет, {user.username}, пожалуйста, подтвердите свой email, перейдя по ссылке: {link}"

    # Отправка письма
    send_mail(subject, message, 'noreply@example.com', [user.email])
