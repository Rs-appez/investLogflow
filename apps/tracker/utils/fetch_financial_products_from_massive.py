import time
from collections.abc import Generator

import requests
from django.conf import settings

MASSIVE_API_URL = "https://api.massive.com/v3/reference/tickers"


def fetch_financial_products_from_massive() -> Generator[dict[str, object], None, None]:
    url = MASSIVE_API_URL
    parameters = {"limit": 1000, "market": "stocks", "apiKey": settings.MASSIVE_API_KEY}
    page = 0
    while url:
        try:
            response = requests.get(
                MASSIVE_API_URL,
                params=parameters,
                timeout=10,
            )
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)
                continue
            response.raise_for_status()
            data = response.json()
            page += 1

            for item in data.get("results", []):
                yield item

            print(f"Fetched page {page} with {len(data.get('results', []))} items.")

            url = data.get("next_url", None)

        except requests.RequestException as e:
            print(f"Error fetching data from Massive: {e}")
            return
