from cachetools import TTLCache

api_cache = TTLCache(maxsize=128, ttl=600)