from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
) -> None:
    """
    Отправляет письмо о сбросе пароля
    Когда создается токен - отправляется письмо
    :param sender: Класс который отправил сигнал
    :param instance: Экземпляр который отправил сигнал
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }
    email_html_message = render_to_string("email/password_reset_email.html", context)
    message = EmailMessage(
        "Сброс пароля для социальной сети 'WEB'",
        email_html_message,
        "noreply@web.ru",
        [reset_password_token.user.email],
    )
    message.send()
