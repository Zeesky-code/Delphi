import httpx
from ..core.config import settings
from cachetools import cached
from ..core.cache import api_cache 

NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

@cached(api_cache)
async def fetch_news(query: str) -> list[dict]:
    """
    Fetches recent news articles for a given query from NewsAPI.
    """
    if not settings.NEWS_API_KEY:
        print("Error: NEWS_API_KEY not set.")
        return []

    params = {
        "q": query,
        "apiKey": settings.NEWS_API_KEY,
        "pageSize": 5, 
        "sortBy": "publishedAt",
        "language": "en"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NEWS_API_BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = [
                {"source": article["source"]["name"], "title": article["title"], "content": article.get("content", "")}
                for article in data.get("articles", [])
            ]
            return articles

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []