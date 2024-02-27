from django.db import models

from communities.models import Community
from users.models import User


class Post(models.Model):
    """Модель поста."""

    author = models.ForeignKey(
        User,
        verbose_name="Автор поста",
        related_name="posts",
        on_delete=models.CASCADE,
    )
    publish_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    communities = models.ManyToManyField(
        Community,
        verbose_name="Сообщества, куда отправили пост",
        related_name="posts",
        blank=True,
    )
    text = models.TextField(
        verbose_name="Текст поста",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Картинка в посте",
        upload_to="posts/image",
        blank=True,
        null=True,
    )
    likes = models.ManyToManyField(
        User,
        through="Like",
        verbose_name="Лайки",
        related_name="liked",
        blank=True,
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = [
            "-publish_date",
        ]


class Like(models.Model):
    user = models.ForeignKey(User, related_name="who_liked", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="what_liked", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
