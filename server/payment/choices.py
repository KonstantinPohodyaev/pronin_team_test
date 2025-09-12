from django.db import models


class ReasonChoices(models.TextChoices):
    """Choices for reason field of Collect model."""

    birthday = 'BIRTHDAY', 'birthday'
    wedding = 'WEDDING', 'wedding'
    charity = 'CHARITY', 'charity'
