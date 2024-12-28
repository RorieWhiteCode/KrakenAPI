# tests/test_data_handler.py
import unittest
from unittest.mock import patch
from data_handler import KrakenDataHandler


class TestDataHandler(unittest.TestCase):
    @patch('data_handler.KrakenDataHandler.get_balance')
    def test_get_balance(self, mock_get_balance):
        mock_get_balance.return_value = {'USD': '1000.0'}
        handler = KrakenDataHandler()
        balance = handler.get_balance()
        self.assertIn('USD', balance)
        self.assertEqual(balance['USD'], '1000.0')

    @patch('data_handler.KrakenDataHandler.get_ticker')
    def test_get_ticker(self, mock_get_ticker):
        mock_get_ticker.return_value = {'ADAUSD': {'c': ['1.25']}}
        handler = KrakenDataHandler()
        ticker = handler.get_ticker('ADAUSD')
        self.assertIn('ADAUSD', ticker)
        self.assertEqual(ticker['ADAUSD']['c'][0], '1.25')


if __name__ == '__main__':
    unittest.main()
