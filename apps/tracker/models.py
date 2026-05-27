import json
from collections import defaultdict
from datetime import date, timedelta
from typing import override

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

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


class PriceRecord(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    close_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    date_recorded = models.DateTimeField()

    class Meta:
        unique_together = ("product", "date_recorded")
        ordering = ["-date_recorded"]

    @override
    def __str__(self):
        return f"Price of {self.product.name} on {self.date_recorded}"


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="portfolios"
    )

    all_dates = []
    all_dates_str = []
    value_per_date = []
    value_per_date_str = []
    buy_per_date = []
    buy_per_date_str = []

    @override
    def __str__(self):
        return self.name

    def add_price_stats(self, nb_days: int):
        time_threshold = timezone.now() - timedelta(days=nb_days - 1)
        self.all_dates = [
            (time_threshold + timedelta(days=day)).date() for day in range(nb_days)
        ]
        investments = self.investments.all()  # pyright: ignore[reportAttributeAccessIssue]
        self.buy_per_date, self.value_per_date = self.__get_value_per_date(
            self.all_dates, investments
        )

        self.__dumps_data()

    def __get_value_per_date(
        self, date_span: list[date], investments: QuerySet[Investment, Investment]
    ) -> tuple[list[float], list[float]]:
        """
        For each date in date_span, calculate the total value of the portfolio based on:
        """
        invested = []
        results = []

        product_ids = investments.values_list("product", flat=True).distinct()

        inv_map: defaultdict[int, list[tuple[date, float, float]]] = defaultdict(list)
        for inv in investments.order_by("date_invested"):
            inv_map[inv.product_id].append(  # pyright: ignore[reportAttributeAccessIssue]
                (
                    inv.date_invested.date(),
                    float(inv.quantity),
                    float(inv.amount_invested_per_share),
                )
            )

        all_prices = (
            PriceRecord.objects.filter(
                product__in=product_ids,
                date_recorded__date__lte=date_span[-1],
            )
            .order_by("product", "date_recorded")
            .values("product", "close_price", "date_recorded")
        )
        price_map: defaultdict[int, list[tuple[date, float]]] = defaultdict(list)
        for record in all_prices:
            price_map[record["product"]].append(
                (record["date_recorded"].date(), float(record["close_price"]))
            )

        inv_ptrs = {pid: 0 for pid in product_ids}
        holdings = {pid: 0.0 for pid in product_ids}
        total_invested = 0.0

        for current_date in date_span:
            for pid in product_ids:
                invs = inv_map[pid]
                while (
                    inv_ptrs[pid] < len(invs) and invs[inv_ptrs[pid]][0] <= current_date
                ):
                    holdings[pid] += invs[inv_ptrs[pid]][1]
                    total_invested += invs[inv_ptrs[pid]][2] * invs[inv_ptrs[pid]][1]
                    inv_ptrs[pid] += 1

            total_value = 0.0
            for pid in product_ids:
                qty = holdings[pid]
                price = 0.0
                for price_date, close_price in reversed(price_map[pid]):
                    if price_date <= current_date:
                        price = close_price
                        break
                total_value += qty * price
            results.append(total_value)
            invested.append(total_invested)
        return invested, results

    def __dumps_data(self):
        self.all_dates_str = json.dumps(self.all_dates, default=str)
        self.value_per_date_str = json.dumps(self.value_per_date, default=str)
        self.buy_per_date_str = json.dumps(self.buy_per_date, default=str)


class Investment(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount_invested_per_share = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=24, decimal_places=6)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="investments"
    )
    date_invested = models.DateTimeField(default=timezone.now)

    @override
    def __str__(self):
        return f"Investment in {self.product.name} on {self.date_invested}"
