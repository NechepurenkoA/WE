from django.db import models

from users.models import User


class Community(models.Model):
    """Модель группы/сообщества."""

    title = models.CharField(
        verbose_name="Название сообщества",
        max_length=35,
    )
    slug = models.SlugField(
        verbose_name="Псевдоним сообщества",
        unique=True,
        max_length=35,
    )
    creator = models.ForeignKey(
        User,
        related_name="creator",
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        verbose_name="Описание сообщества",
        max_length=150,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="Аватар сообщества",
        upload_to="community/avatar",
        blank=True,
        null=True,
    )
    followers = models.ManyToManyField(
        User,
        verbose_name="Подписчики",
        related_name="followers",
        blank=True,
    )

    @property
    def get_followers_amount(self) -> int:
        """Метод для получения кол-ва подписчиков."""
        return self.followers.all().count()

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"
        ordering = [
            "slug",
        ]
