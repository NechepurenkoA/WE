import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import Sex


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


class Group(models.Model):
    """Модель группы/сообщества."""

    title = models.CharField(verbose_name="Название группы", max_length=35)
    slug = models.SlugField(verbose_name="Псевдоним группы", unique=True, max_length=35)
    creator = models.ForeignKey(
        "User",
        related_name="creator",
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        verbose_name="Описание группы",
        max_length=150,
        blank=True,
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = [
            "slug",
        ]
