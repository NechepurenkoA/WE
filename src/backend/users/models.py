import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import FriendRequestStatus, Sex


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name="Эл. почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
    )
    sex = models.TextField(
        verbose_name="Пол",
        choices=Sex,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="user/avatar",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True,
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        null=True,
        blank=True,
    )
    biography = models.TextField(
        verbose_name="О себе",
        blank=True,
        max_length=150,
    )
    # WIP
    # friends = models.ManyToManyField(...)

    @property
    def get_age(self):
        today = datetime.date.today()
        if self.birth_date is not None:
            age = int(
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
            return age
        return None

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "username",
        ]


# WIP, examply only
class FriendRequest(models.Model):
    """Модель запроса в друзья."""

    status = models.IntegerField(
        choices=FriendRequestStatus,
        default=1,
    )
    sender = models.ForeignKey(
        User,
        related_name="requests_sent",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        related_name="requests_received",
        on_delete=models.CASCADE,
    )
    sent_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Запрос дружбы"
        verbose_name_plural = "Запросы дружбы"
        ordering = [
            "sent_on",
        ]


# WIP, example only
class Friendship(models.Model):
    """Модель дружбы между пользователями."""

    users = models.ManyToManyField(
        User,
        related_name="friends",
    )
    current_user = models.ForeignKey(
        User,
        related_name="owner",
        on_delete=models.CASCADE,
    )
    friends_from = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"
        ordering = [
            "friends_from",
        ]
