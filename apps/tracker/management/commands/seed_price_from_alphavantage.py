from typing import override

from django.core.management.base import BaseCommand

from apps.tracker.models import PriceRecord, Stock
from apps.tracker.utils import fetch_price_data_from_alphavantage


class Command(BaseCommand):
    help = "Seed the database with price data from Alpha Vantage"

    @override
    def add_arguments(self, parser):
        _ = parser.add_argument(
            "--force", action="store_true", help="Re-fetch even if data exists"
        )

    @override
    def handle(self, *args, **options):
        if PriceRecord.objects.exists() and not options["force"]:
            self.stdout.write(
                self.style.WARNING(
                    "Price data already exists. Use --force to re-fetch."
                )
            )
            return
        try:
            for stock in Stock.objects.all()[:2]:  # Limit to first 2 stocks for testing
                price_data = fetch_price_data_from_alphavantage(
                    stock.ticker
                )  # Limited api can only make 25 calls per day
                records = [
                    PriceRecord(
                        product=stock,
                        date_recorded=date_str,
                        open_price=daily_data["open"],
                        high_price=daily_data["high"],
                        low_price=daily_data["low"],
                        close_price=daily_data["close"],
                        volume=daily_data["volume"],
                    )
                    for date_str, daily_data in price_data.items()
                ]
                _ = PriceRecord.objects.bulk_create(records, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS("Price data seeded successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
