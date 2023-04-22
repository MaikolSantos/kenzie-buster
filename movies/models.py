from django.db import models
from users.models import User


class Rating(models.TextChoices):
    GENERAL_AUDIENCES = "G"
    PARENTAL_GUIDANCE_SUGGESTED = "PG"
    PARENTS_STRONGLY_CAUTIONED = "PG-13"
    RESTRICTED = "R"
    ADULTS_ONLY = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(
        max_length=10, null=True, blank=True, default=None
    )
    rating = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=Rating.choices,
        default=Rating.GENERAL_AUDIENCES,
    )
    synopsis = models.TextField(null=True, blank=True, default=None)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies",
        null=True
    )
