from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Choices for transaction category — used in the chart and filter views
CATEGORY_CHOICES = [
    ('rent', 'Rent'),
    ('groceries', 'Groceries'),
    ('entertainment', 'Entertainment'),
    ('transport', 'Transport'),
    ('utilities', 'Utilities'),
    ('health', 'Health'),
    ('income', 'Income'),
    ('other', 'Other'),
]


class Transaction(models.Model):
    """
    Represents a single financial transaction for a user.
    Each transaction has an amount, category, description, and date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    is_income = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} | {self.category} | ${self.amount:.2f}"

    def signed_amount(self):
        """Return positive amount for income, negative for expense."""
        return self.amount if self.is_income else -self.amount
