import krakenex
import time

# Initialize Kraken API
api = krakenex.API()
api.load_key('kraken.key')  # File containing your Kraken API key and secret

# Fetch account balance
def get_balance():
    try:
        balance = api.query_private('Balance')
        if balance.get('error'):
            print("Error:", balance['error'])
        else:
            print("Account Balance:", balance['result'])
    except Exception as e:
        print("Error fetching balance:", e)

# Fetch ticker information
def get_ticker(pair):
    try:
        ticker = api.query_public('Ticker', {'pair': pair})
        if ticker.get('error'):
            print("Error:", ticker['error'])
        else:
            print("Ticker Info:", ticker['result'])
    except Exception as e:
        print("Error fetching ticker:", e)

# Example Usage
get_balance()
get_ticker('XXBTZUSD')  # Example pair for Bitcoin to USD
