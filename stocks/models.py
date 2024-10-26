from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ticker

    def save(self, *args, **kwargs):
        self.ticker = self.ticker.upper()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE_CHOICES, default="buy"
    )
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    price_per_share = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.stock = self.stock.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stock.ticker} on {self.date}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.stock.ticker} on {self.date}, {self.quantity} shares"


class InvestmentReturn(models.Model):
    INVESTMENT_TYPE = [
        ("long-term", "Long-Term"),
        ("short-term", "Short-Term"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=10, choices=INVESTMENT_TYPE)
    gain_loss_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.stock.ticker} on {self.date}, {self.sale_proceeds} proceeds"
