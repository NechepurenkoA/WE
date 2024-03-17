from django.db import models


class Gender(models.TextChoices):
    MALE = (
        "Парень",
        "Парень",
    )
    FEMALE = (
        "Девушка",
        "Девушка",
    )
