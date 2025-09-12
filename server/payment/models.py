from typing import override

from django.db import models
from django.contrib.auth import get_user_model

from server.payment.choices import ReasonChoices

User = get_user_model()


class DateTimeBaseModel(models.Model):
    """Base model for creating created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payment(DateTimeBaseModel):
    """Model for payment`s logic."""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    amount = models.DecimalField(
        'Amount of money',
        max_digits=10,
        decimal_places=2,
    )
    comment = models.TextField('User`s comment')
    collect = models.ForeignKey(
        to='payment.Collect',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ('amount', 'comment')
        default_related_name = '%(class)ss'

    @override
    def __str__(self):
        """Method for display short info of payment instance."""
        return f'{self.collect.title}: {self.amount}'


class Collect(DateTimeBaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    title = models.CharField(
        'Title of collect',
        max_length=128,
        unique=True,
    )
    reason = models.CharField(
        'Reason',
        max_length=128,
        choices=ReasonChoices.choices,
    )
    description = models.TextField('description')
    target_amount = models.DecimalField(
        'Target amount',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    current_amount = models.DecimalField(
        'Current amount',
        max_digits=20,
        decimal_places=2
    )
    donators_count = models.PositiveIntegerField('Donators count')
    image = models.ImageField(
        'Image',
        upload_to='media/collect_image',
    )

    class Meta:
        verbose_name = 'Collect'
        verbose_name_plural = 'Collects'
        ordering = ('title', 'target_amount', 'current_amount')

    @override
    def __str__(self):
        """Method for display short info of collect instance."""
        return f'{self.title}: {self.current_amount}/{self.target_amount}'
