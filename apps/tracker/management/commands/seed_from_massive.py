from typing import override

from django.core.management.base import BaseCommand

from apps.tracker.models import Stock
from apps.tracker.utils import fetch_financial_products_from_massive


class Command(BaseCommand):
    help = "Seed the database with financial products from Massive"

    @override
    def add_arguments(self, parser):
        _ = parser.add_argument(
            "--force", action="store_true", help="Re-fetch even if data exists"
        )

    @override
    def handle(self, *args, **options):
        if Stock.objects.exists() and not options["force"]:
            self.stdout.write(
                self.style.WARNING(
                    "Financial products already exist. Use --force to re-fetch."
                )
            )
            return
        try:
            data_fetch = fetch_financial_products_from_massive()
            nb_created = 0
            nb_updated = 0
            for item in data_fetch:
                if item.get("market") == "stocks":
                    _, created = Stock.objects.update_or_create(
                        ticker=item.get("ticker"),
                        defaults={
                            "name": item.get("name", ""),
                            "active": item.get("active", False),
                            "cik": item.get("cik", ""),
                            "currency": item.get("currency", ""),
                            "primary_exchange": item.get("primaryExchange", ""),
                            "composite_figi": item.get("compositeFigi", ""),
                            "share_class_figi": item.get("shareClassFigi", ""),
                        },
                    )
                    if created:
                        nb_created += 1
                    else:
                        nb_updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished fetching data. Created: {nb_created}, Updated: {nb_updated}"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
