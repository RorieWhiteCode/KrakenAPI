# collector.py
import requests
import asyncio
from typing import Dict, Any, List
import time


class NewsCollector:
    """Fetch sentiment data from news sources."""
    def __init__(self):
        self.sources = {
            "CryptoPanic": "https://cryptopanic.com/api/v1/posts/?auth_token=your_api_key",
            "NewsAPI": "https://newsapi.org/v2/everything?q=crypto&apiKey=your_api_key"
        }
    
    def fetch_news(self) -> Dict[str, Any]:
        results = {}
        for source, url in self.sources.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    results[source] = response.json()
                else:
                    print(f"[WARNING] Failed to fetch from {source}. Status Code: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] Error fetching data from {source}: {e}")
        return results


class SocialMediaCollector:
    """Fetch sentiment data from social media sources like Twitter and Reddit."""
    def __init__(self):
        self.sources = {
            "Twitter": "https://api.twitter.com/2/tweets/search/recent",
            "Reddit": "https://www.reddit.com/r/cryptocurrency.json"
        }
        self.headers = {
            "Twitter": {"Authorization": "Bearer your_twitter_api_key"},
            "Reddit": {"User-Agent": "Mozilla/5.0"}
        }
    
    def fetch_social_media(self) -> Dict[str, Any]:
        results = {}
        for source, url in self.sources.items():
            try:
                response = requests.get(url, headers=self.headers.get(source, {}))
                if response.status_code == 200:
                    results[source] = response.json()
                else:
                    print(f"[WARNING] Failed to fetch from {source}. Status Code: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] Error fetching data from {source}: {e}")
        return results


class ExpertCollector:
    """Fetch price predictions and insights from expert sources."""
    def __init__(self):
        self.sources = {
            "TradingView": "https://api.tradingview.com/predictions",
            "Glassnode": "https://api.glassnode.com/v1/metrics"
        }
    
    def fetch_expert_predictions(self) -> Dict[str, Any]:
        results = {}
        for source, url in self.sources.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    results[source] = response.json()
                else:
                    print(f"[WARNING] Failed to fetch from {source}. Status Code: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] Error fetching data from {source}: {e}")
        return results


class SentimentCollector:
    """Master class for collecting all sentiment data."""
    def __init__(self):
        self.news_collector = NewsCollector()
        self.social_media_collector = SocialMediaCollector()
        self.expert_collector = ExpertCollector()
        self.data = {}
    
    async def fetch_all_data(self):
        """Fetch all sentiment data asynchronously."""
        tasks = [
            asyncio.to_thread(self.news_collector.fetch_news),
            asyncio.to_thread(self.social_media_collector.fetch_social_media),
            asyncio.to_thread(self.expert_collector.fetch_expert_predictions)
        ]
        results = await asyncio.gather(*tasks)
        
        self.data['news'] = results[0]
        self.data['social_media'] = results[1]
        self.data['expert_predictions'] = results[2]
    
    def get_data(self) -> Dict[str, Any]:
        """Return all collected sentiment data."""
        return self.data


# Example Usage
if __name__ == '__main__':
    collector = SentimentCollector()
    
    print("[INFO] Starting data collection...")
    asyncio.run(collector.fetch_all_data())
    
    data = collector.get_data()
    print("[INFO] Collected Sentiment Data:")
    print(data)
