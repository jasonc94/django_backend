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
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.stock = self.stock.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stock} transaction on {self.date}"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    remaining_quantity = models.FloatField()
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.stock.ticker} on {self.date}, {self.quantity} shares"


class InvestmentReturn(models.Model):
    INVESTMENT_TYPE = [
        ("long-term", "Long-Term"),
        ("short-term", "Short-Term"),
    ]

    holding = models.ForeignKey(Holding, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    purchase_date = models.DateTimeField()
    sell_date = models.DateTimeField()
    investment_type = models.CharField(max_length=10, choices=INVESTMENT_TYPE)
    gain_loss_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.ticker} {self.investment_type} investment on {self.purchase_date}"
