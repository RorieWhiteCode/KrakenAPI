# tests/test_strategy.py
import unittest
from unittest.mock import patch
from strategy import Strategy


class TestStrategy(unittest.TestCase):
    @patch('strategy.Strategy.rsi_strategy')
    def test_rsi_strategy(self, mock_rsi_strategy):
        mock_rsi_strategy.return_value = 'buy'
        strategy = Strategy()
        signal = strategy.rsi_strategy('ADAUSD')
        self.assertEqual(signal, 'buy')

    @patch('strategy.Strategy.ma_strategy')
    def test_ma_strategy(self, mock_ma_strategy):
        mock_ma_strategy.return_value = 'sell'
        strategy = Strategy()
        signal = strategy.ma_strategy('ADAUSD')
        self.assertEqual(signal, 'sell')


if __name__ == '__main__':
    unittest.main()
