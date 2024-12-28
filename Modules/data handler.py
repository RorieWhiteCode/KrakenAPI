# data_handler.py
import krakenex
import time
import pandas as pd
from typing import Dict, Union

# Import configuration settings
from config import API_KEY, API_SECRET, ALLOWED_PAIRS, API_CALL_DELAY


class KrakenDataHandler:
    def __init__(self):
        # Set up Kraken API with credentials
        self.api = krakenex.API()
        self.api.key = API_KEY
        self.api.secret = API_SECRET

    def get_balance(self) -> Dict[str, Union[str, float]]:
        # Fetch the current account balance from Kraken
        try:
            response = self.api.query_private('Balance')
            if response.get('error'):
                raise Exception(response['error'])
            return response['result']
        except Exception as e:
            print(f"[ERROR] Could not retrieve account balance: {e}")
            return {}

    def get_ticker(self, pair: str) -> Dict[str, Union[str, float]]:
        # Get live ticker data for a trading pair (e.g., ADAUSD)
        try:
            response = self.api.query_public('Ticker', {'pair': pair})
            if response.get('error'):
                raise Exception(response['error'])
            return response['result']
        except Exception as e:
            print(f"[ERROR] Failed to fetch ticker data for {pair}: {e}")
            return {}

    def get_ohlc(self, pair: str, interval: int = 60) -> pd.DataFrame:
        # Fetch historical OHLC data for a trading pair
        try:
            response = self.api.query_public('OHLC', {'pair': pair, 'interval': interval})
            if response.get('error'):
                raise Exception(response['error'])
            data = response['result'][pair]
            df = pd.DataFrame(data, columns=[
                'time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
            ])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            print(f"[ERROR] Failed to fetch OHLC data for {pair}: {e}")
            return pd.DataFrame()

    def get_open_orders(self) -> Dict[str, Union[str, float]]:
        # Retrieve any currently open orders
        try:
            response = self.api.query_private('OpenOrders')
            if response.get('error'):
                raise Exception(response['error'])
            return response['result']['open']
        except Exception as e:
            print(f"[ERROR] Could not retrieve open orders: {e}")
            return {}

    def get_trade_history(self) -> Dict[str, Union[str, float]]:
        # Fetch the account's trade history
        try:
            response = self.api.query_private('TradesHistory')
            if response.get('error'):
                raise Exception(response['error'])
            return response['result']['trades']
        except Exception as e:
            print(f"[ERROR] Failed to retrieve trade history: {e}")
            return {}


# Example usage for testing the functions
if __name__ == '__main__':
    handler = KrakenDataHandler()
    
    print("Fetching account balance...")
    balance = handler.get_balance()
    print(balance)
    
    print("\nFetching ADA/USD ticker data...")
    ticker = handler.get_ticker('ADAUSD')
    print(ticker)
    
    print("\nFetching OHLC data for ADA/USD...")
    ohlc_data = handler.get_ohlc('ADAUSD', interval=60)
    print(ohlc_data.head())
    
    print("\nFetching open orders...")
    open_orders = handler.get_open_orders()
    print(open_orders)
    
    print("\nFetching trade history...")
    trade_history = handler.get_trade_history()
    print(trade_history)
