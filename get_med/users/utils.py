from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_confirmation_token


def send_confirmation_email(request, user):
    token = email_confirmation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)

    confirm_url = reverse('confirm_email', kwargs={
        'uidb64': uid,
        'token': token,
    })

    link = f"http://{current_site.domain}{confirm_url}"

    subject = 'Подтверждение электронной почты'
    message = f"Привет, {user.username}, пожалуйста, подтвердите свой email, перейдя по ссылке: {link}"

    send_mail(subject, message, 'noreply@example.com', [user.email])
