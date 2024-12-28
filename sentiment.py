# sentiment_analyzer.py
import requests
from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        self.news_api = "https://newsapi.org/v2/everything"
        self.api_key = "your_news_api_key"

    def fetch_news(self, keyword: str):
        response = requests.get(f"{self.news_api}?q={keyword}&apiKey={self.api_key}")
        if response.status_code != 200:
            print("[ERROR] Failed to fetch news.")
            return []
        return response.json().get('articles', [])

    def analyze_sentiment(self, text: str):
        sentiment = TextBlob(text).sentiment.polarity
        return sentiment

    def get_sentiment_score(self, keyword: str):
        articles = self.fetch_news(keyword)
        if not articles:
            return 0
        scores = [self.analyze_sentiment(article['title']) for article in articles]
        return sum(scores) / len(scores)


if __name__ == '__main__':
    analyzer = SentimentAnalyzer()
    score = analyzer.get_sentiment_score('ADA')
    print(f"[INFO] Sentiment Score for ADA: {score}")
