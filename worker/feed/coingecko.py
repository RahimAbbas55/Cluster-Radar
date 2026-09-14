import time
import requests
from .base import FeedChecker

class CoinGeckoChecker(FeedChecker):
    name = "coingecko"
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    def fetch(self):
        start = time.monotonic()
        try:
            response = requests.get(self.url, timeout=5)
            latency_ms = (time.monotonic() - start) * 1000
            response.raise_for_status()
            price = response.json()["bitcoin"]["usd"]
            return price, latency_ms, None
        except Exception as e:
            latency_ms = (time.monotonic() - start) * 1000
            return None, latency_ms, str(e)