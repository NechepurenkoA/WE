from django.db import models


class Sex(models.TextChoices):
    MALE = (
        "Парень",
        "Парень",
    )
    FEMALE = (
        "Девушка",
        "Девушка",
    )
