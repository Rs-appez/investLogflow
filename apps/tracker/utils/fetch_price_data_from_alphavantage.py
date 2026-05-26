import requests
from django.conf import settings


ALPHAVANTAGE_API_URL = "https://www.alphavantage.co/query"


def fetch_price_data_from_alphavantage(ticker: str) -> dict:

    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": settings.ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact",
        "datatype": "json",
    }
    try:
        response = requests.get(ALPHAVANTAGE_API_URL, params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "Time Series (Daily)" in data:
            return {
                date: {
                    "open": float(daily_data["1. open"]),
                    "high": float(daily_data["2. high"]),
                    "low": float(daily_data["3. low"]),
                    "close": float(daily_data["4. close"]),
                    "volume": int(daily_data["5. volume"]),
                }
                for date, daily_data in data["Time Series (Daily)"].items()
            }
        else:
            raise ValueError(f"Unexpected response format: {data}")
    except requests.RequestException as e:
        print(f"Error fetching price data for {ticker}: {e}")
        return {}
