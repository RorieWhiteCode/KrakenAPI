# processor.py
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from typing import Dict, Any

# Download required NLTK datasets for text processing
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Handles text normalization and preprocessing
class TextProcessor:
    def __init__(self):
        # Initialize stopwords and lemmatizer
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    # Clean and preprocess text data
    def clean_text(self, text: str) -> str:
        text = text.lower()  # Convert text to lowercase
        text = re.sub(r'https?:\/\/\S+', '', text)  # Remove URLs
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
        tokens = word_tokenize(text)  # Tokenize text into words
        tokens = [word for word in tokens if word not in self.stop_words]  # Remove stopwords
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize tokens
        return ' '.join(tokens)  # Return cleaned text


# Processes raw sentiment data into structured formats
class DataProcessor:
    def __init__(self):
        # Initialize text processor
        self.text_processor = TextProcessor()
    
    # Process news data and extract relevant fields
    def process_news_data(self, news_data: Dict[str, Any]) -> pd.DataFrame:
        records = []
        for source, articles in news_data.items():
            for article in articles.get('results', []):
                records.append({
                    'source': source,
                    'type': 'news',
                    'title': self.text_processor.clean_text(article.get('title', '')),
                    'summary': self.text_processor.clean_text(article.get('description', '')),
                    'url': article.get('url', ''),
                    'timestamp': article.get('published_at', '')
                })
        return pd.DataFrame(records)
    
    # Process social media data from Twitter and Reddit
    def process_social_data(self, social_data: Dict[str, Any]) -> pd.DataFrame:
        records = []
        for source, posts in social_data.items():
            if source == 'Twitter':
                for tweet in posts.get('data', []):
                    records.append({
                        'source': source,
                        'type': 'social',
                        'content': self.text_processor.clean_text(tweet.get('text', '')),
                        'timestamp': tweet.get('created_at', '')
                    })
            elif source == 'Reddit':
                for post in posts.get('data', {}).get('children', []):
                    records.append({
                        'source': source,
                        'type': 'social',
                        'content': self.text_processor.clean_text(post.get('data', {}).get('title', '')),
                        'timestamp': post.get('data', {}).get('created_utc', '')
                    })
        return pd.DataFrame(records)
    
    # Process expert predictions from analytics sources
    def process_expert_data(self, expert_data: Dict[str, Any]) -> pd.DataFrame:
        records = []
        for source, predictions in expert_data.items():
            records.append({
                'source': source,
                'type': 'expert',
                'prediction': predictions.get('price_target', ''),
                'confidence': predictions.get('confidence', ''),
                'timestamp': predictions.get('timestamp', '')
            })
        return pd.DataFrame(records)


# Coordinates preprocessing of all sentiment data sources
class SentimentPreprocessor:
    def __init__(self):
        # Initialize data processor
        self.data_processor = DataProcessor()
    
    # Preprocess raw data from all sources into a unified DataFrame
    def preprocess_all(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        news_df = self.data_processor.process_news_data(raw_data.get('news', {}))
        social_df = self.data_processor.process_social_data(raw_data.get('social_media', {}))
        expert_df = self.data_processor.process_expert_data(raw_data.get('expert_predictions', {}))
        
        # Combine all data into one structured DataFrame
        combined_df = pd.concat([news_df, social_df, expert_df], ignore_index=True)
        print(f"[INFO] Preprocessed {len(combined_df)} sentiment records.")
        return combined_df


# Example Usage
if __name__ == '__main__':
    # Mock raw sentiment data (replace with real data from collector.py)
    raw_data = {
        'news': {
            'CryptoPanic': {
                'results': [
                    {'title': 'Market Surges', 'description': 'Crypto market rises by 10%', 'url': 'http://news.com/article1', 'published_at': '2024-06-28'}
                ]
            }
        },
        'social_media': {
            'Twitter': {
                'data': [
                    {'text': 'Bitcoin is mooning!', 'created_at': '2024-06-28T12:00:00Z'}
                ]
            },
            'Reddit': {
                'data': {
                    'children': [
                        {'data': {'title': 'ETH going to $10K!', 'created_utc': '2024-06-28T12:30:00Z'}}
                    ]
                }
            }
        },
        'expert_predictions': {
            'TradingView': {
                'price_target': '50000',
                'confidence': '0.85',
                'timestamp': '2024-06-28T13:00:00Z'
            }
        }
    }
    
    # Preprocess sentiment data
    preprocessor = SentimentPreprocessor()
    processed_data = preprocessor.preprocess_all(raw_data)
    print(processed_data)
