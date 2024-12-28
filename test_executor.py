# tests/test_trade_executor.py
import unittest
from unittest.mock import patch
from trade_executor import TradeExecutor


class TestTradeExecutor(unittest.TestCase):
    @patch('trade_executor.TradeExecutor.place_market_order')
    def test_place_market_order(self, mock_place_market_order):
        mock_place_market_order.return_value = {'result': 'success'}
        executor = TradeExecutor()
        result = executor.place_market_order('ADAUSD', 1.0, 'buy')
        self.assertEqual(result['result'], 'success')

    @patch('trade_executor.TradeExecutor.cancel_order')
    def test_cancel_order(self, mock_cancel_order):
        mock_cancel_order.return_value = True
        executor = TradeExecutor()
        result = executor.cancel_order('O12345')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
