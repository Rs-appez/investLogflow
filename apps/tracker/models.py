from typing import override

from django.db import models

from apps.users.models import Organization


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=50)
    active = models.BooleanField()
    cik = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    primary_exchange = models.CharField(max_length=255)
    composite_figi = models.CharField(max_length=12)
    share_class_figi = models.CharField(max_length=12)

    @override
    def __str__(self):
        return f"{self.name} ({self.ticker})"


class ActualPrice(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_recorded = models.DateTimeField(auto_now_add=True)

    @override
    def __str__(self):
        return f"Price of {self.product.name} on {self.date_recorded}: {self.price}"


class Investment(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=24, decimal_places=6)
    date_invested = models.DateTimeField(auto_now_add=True)

    @override
    def __str__(self):
        return f"Investment in {self.product.name} on {self.date_invested}"


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    investments = models.ManyToManyField(Investment, related_name="portfolios")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="portfolios"
    )

    @override
    def __str__(self):
        return self.name
