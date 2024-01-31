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


class FriendRequestStatus(models.IntegerChoices):
    PENDING = (1, "Pending")
    ACCEPTED = (2, "Accepted")
    REJECTED = (3, "Rejected")
