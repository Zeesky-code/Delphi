import httpx
from ..core.config import settings
from ..core.cache import api_cache
from cachetools import cached 
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

@cached(api_cache)
async def fetch_company_overview(ticker: str) -> dict:
    print(f"--- CACHE MISS: Fetching Company Overview for '{ticker}' from API. ---")
    """
    Fetches company overview and key financial metrics from Alpha Vantage.
    """
    if not settings.ALPHA_VANTAGE_API_KEY:
        print("Error: ALPHA_VANTAGE_API_KEY not set.")
        return {}

    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ALPHA_VANTAGE_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                print(f"Warning: No data found for ticker {ticker}.")
                return {}
            
            return data

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred while fetching financial data: {e}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

@cached(api_cache)
async def fetch_historical_prices(ticker: str) -> list[dict]:
    """
    Fetches daily historical stock prices for a given ticker from Alpha Vantage.
    """
    print(f"--- CACHE MISS: Fetching historical prices for '{ticker}' from API. ---")
    if not settings.ALPHA_VANTAGE_API_KEY:
        print("Error: ALPHA_VANTAGE_API_KEY not set.")
        return []

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": settings.ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact" 
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ALPHA_VANTAGE_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            time_series = data.get("Time Series (Daily)", {})
            prices = [
                {"date": date, "close": float(details["4. close"])}
                for date, details in time_series.items()
            ]
            return prices

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred while fetching historical data: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []