# tests/test_portfolio.py
import unittest
from portfolio import PortfolioManager


class TestPortfolioManager(unittest.TestCase):
    def setUp(self):
        self.portfolio = PortfolioManager()

    def test_update_balance(self):
        self.portfolio.balance = {'USD': '1000.0'}
        self.portfolio.update_balance()
        self.assertIn('USD', self.portfolio.balance)

    def test_add_position(self):
        self.portfolio.add_position('ADA/USD', 100)
        self.assertIn('ADA/USD', self.portfolio.positions)
        self.assertEqual(self.portfolio.positions['ADA/USD']['amount'], 100)


if __name__ == '__main__':
    unittest.main()
