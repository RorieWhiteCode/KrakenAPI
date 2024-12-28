# trade_executor.py
import time
import krakenex
from typing import Dict, Union
from config import API_KEY, API_SECRET, ORDER_TYPE, API_CALL_DELAY


class TradeExecutor:
    def __init__(self):
        # Initialize Kraken API
        self.api = krakenex.API()
        self.api.key = API_KEY
        self.api.secret = API_SECRET
        self.retry_attempts = 3  # Number of retries for failed orders

    # Place a market order
    def place_market_order(self, pair: str, volume: float, side: str) -> Union[Dict, None]:
        """
        Place a market order (buy/sell) on Kraken.
        """
        order_data = {
            'pair': pair,
            'type': side,  # 'buy' or 'sell'
            'ordertype': 'market',
            'volume': volume
        }
        return self._execute_order(order_data)

    # Place a limit order
    def place_limit_order(self, pair: str, volume: float, side: str, price: float) -> Union[Dict, None]:
        """
        Place a limit order (buy/sell) at a specified price.
        """
        order_data = {
            'pair': pair,
            'type': side,
            'ordertype': 'limit',
            'price': price,
            'volume': volume
        }
        return self._execute_order(order_data)

    # Place a stop-loss order
    def place_stop_loss_order(self, pair: str, volume: float, side: str, stop_price: float) -> Union[Dict, None]:
        """
        Place a stop-loss order to limit losses.
        """
        order_data = {
            'pair': pair,
            'type': side,
            'ordertype': 'stop-loss',
            'price': stop_price,
            'volume': volume
        }
        return self._execute_order(order_data)

    # Execute an order with retry logic
    def _execute_order(self, order_data: Dict) -> Union[Dict, None]:
        """
        Execute an order with retry logic in case of failure.
        """
        attempt = 0
        while attempt < self.retry_attempts:
            try:
                print(f"[INFO] Attempting to place order: {order_data}")
                response = self.api.query_private('AddOrder', order_data)
                if response.get('error'):
                    raise Exception(', '.join(response['error']))
                print(f"[SUCCESS] Order placed successfully: {response['result']}")
                return response['result']
            except Exception as e:
                attempt += 1
                print(f"[ERROR] Failed to place order (Attempt {attempt}): {e}")
                time.sleep(API_CALL_DELAY)

        print("[FATAL] Order failed after multiple attempts.")
        return None

    # Cancel an active order
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an existing order by its ID.
        """
        try:
            print(f"[INFO] Cancelling order: {order_id}")
            response = self.api.query_private('CancelOrder', {'txid': order_id})
            if response.get('error'):
                raise Exception(', '.join(response['error']))
            print(f"[SUCCESS] Order {order_id} cancelled successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to cancel order {order_id}: {e}")
            return False


# Example Usage
if __name__ == '__main__':
    executor = TradeExecutor()
    
    # Place a market buy order
    print("\nPlacing Market Buy Order for ADA/USD...")
    executor.place_market_order(pair='ADAUSD', volume=1.0, side='buy')
    
    # Place a limit sell order
    print("\nPlacing Limit Sell Order for ADA/USD...")
    executor.place_limit_order(pair='ADAUSD', volume=1.0, side='sell', price=0.50)
    
    # Place a stop-loss order
    print("\nPlacing Stop-Loss Order for ADA/USD...")
    executor.place_stop_loss_order(pair='ADAUSD', volume=1.0, side='sell', stop_price=0.45)
    
    # Cancel an order (replace with an actual order ID)
    print("\nCancelling Order...")
    executor.cancel_order(order_id='O12345')
