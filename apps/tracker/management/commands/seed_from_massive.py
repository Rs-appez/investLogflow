from itertools import islice
from typing import override

from django.core.management.base import BaseCommand

from apps.tracker.models import Stock
from apps.tracker.utils import fetch_financial_products_from_massive

BATCH_SIZE = 500


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
            total_created = 0
            total_updated = 0
            gen = fetch_financial_products_from_massive()

            for batch in iter(lambda: list(islice(gen, BATCH_SIZE)), []):
                objs = [
                    Stock(
                        name=item.get("name", ""),
                        ticker=item.get("ticker", ""),
                        active=item.get("active", False),
                        cik=item.get("cik", ""),
                        currency=item.get("currency", ""),
                        primary_exchange=item.get("primary_exchange", ""),
                        composite_figi=item.get("composite_figi", ""),
                        share_class_figi=item.get("share_class_figi", ""),
                    )
                    for item in batch
                ]
                result = Stock.objects.bulk_create(
                    objs,
                    update_conflicts=True,
                    unique_fields=["ticker"],
                    update_fields=[
                        f.name
                        for f in Stock._meta.fields
                        if f.name not in ("id", "ticker")
                    ],
                )
                total_created += sum(1 for obj in result if obj._state.adding)
                total_updated += len(result) - total_created

            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. Seeded {total_created} records, updated {total_updated} records."
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
