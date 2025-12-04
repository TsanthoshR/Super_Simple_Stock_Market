"""Unit tests for the GBCE market behaviors."""

import unittest

from src.stockmarket.exchange.market import GBCE
from src.stockmarket.stock.exceptions import InvalidTradeError, NoTradeError
from src.stockmarket.stock.models import CommonStock, Stock


class TestGBCEMarket(unittest.TestCase):
    """Unit tests for the GBCE market behaviors."""

    def setUp(self):
        """Adding a test stock to the market for testing purposes."""
        self.market = GBCE()

        self.stock_1 = CommonStock(
            symbol="TEST1",
            last_dividend=8.0,
            par_value=100.0,
        )

        self.market.add_Stock(self.stock_1)

    def test_add_stock(self):
        """Verify if test stock was added correctly."""
        with self.assertRaises(TypeError):
            stock = Stock(
                symbol="TEST1",
                type="COMMON",
                last_dividend=8.0,
                par_value=100.0,
            )

            self.market.add_Stock(stock)

        self.assertIn("TEST1", self.market.stocks)

    def test_add_common_stock(self):
        """Verify if test stock was added correctly."""
        retrieved_stock = self.market.get_stock("TEST1")
        self.assertIsNotNone(retrieved_stock)
        self.assertEqual(retrieved_stock.symbol, "TEST1")

        self.assertIn("TEST1", self.market.stocks)

    def test_record_trade(self):
        """Record a trade and verify if it was added correctly."""
        self.market.record_trade(
            symbol="TEST1",
            trade_type="BUY",
            quantity=50,
            price=120.0,
        )

        stock = self.market.get_stock("TEST1")
        self.assertEqual(len(stock.trades), 1)

        trade = stock.trades[0]
        self.assertEqual(trade.quantity, 50)
        self.assertEqual(trade.price, 120.0)
        self.assertEqual(trade.trade_type, "BUY")

    def test_record_trade_no_stock(self):
        """Test recording a trade for a non-existent stock."""
        with self.assertRaises(KeyError):
            self.market.record_trade(
                symbol="NONEXISTENT",
                trade_type="SELL",
                quantity=10,
                price=50.0,
            )

    def test_record_trade_invalid_quantity(self):
        """Test recording a trade with invalid quantity."""
        with self.assertRaises(InvalidTradeError):
            self.market.record_trade(
                symbol="TEST1",
                trade_type="BUY",
                quantity=-10,
                price=100.0,
            )

    def test_volume_weighted_stock_price_no_trades(self):
        """Test VWSP calculation when no trades exist."""
        stock = self.market.get_stock("TEST1")
        with self.assertRaises(NoTradeError):
            stock.calculate_volume_weighted_stock_price(minutes=15)

    def test_volumne_weighted_price_with_trades(self):
        """Test VWSP calculation with existing trades."""
        self.market.record_trade(
            symbol="TEST1",
            trade_type="BUY",
            quantity=100,
            price=110.0,
        )
        self.market.record_trade(
            symbol="TEST1",
            trade_type="SELL",
            quantity=50,
            price=130.0,
        )

        stock = self.market.get_stock("TEST1")
        vwsp = stock.calculate_volume_weighted_stock_price(minutes=15)

        expected_vwsp = (100 * 110.0 + 50 * 130.0) / (100 + 50)
        self.assertAlmostEqual(vwsp, expected_vwsp)

    def test_pe_ratio(self):
        """Test P/E Ratio calculation."""
        stock = self.market.get_stock("TEST1")
        self.market.record_trade(
            symbol="TEST1",
            trade_type="BUY",
            quantity=100,
            price=200.0,
        )

        pe_ratio = stock.calculate_pe_ratio(price=200.0)
        dividend = stock.calculate_dividend_yield(price=200.0) * 200.0
        expected_pe_ratio = 200.0 / dividend
        self.assertAlmostEqual(pe_ratio, expected_pe_ratio)

    def test_dividend_yield(self):
        """Test dividend yield calculation."""
        stock = self.market.get_stock("TEST1")
        dividend_yield = stock.calculate_dividend_yield(price=100.0)
        expected_dividend_yield = stock.last_dividend / 100.0
        self.assertAlmostEqual(dividend_yield, expected_dividend_yield)

    def test_gbce_all_share_index(self):
        """Test GBCE All Share Index calculation."""
        self.market.record_trade(
            symbol="TEST1",
            trade_type="BUY",
            quantity=100,
            price=100.0,
        )

        gbce_index = self.market.calculate_gbce_all_share_index()
        self.assertEqual(gbce_index, 100.0)

    def test_list_stocks(self):
        """Test listing all stocks in the market."""
        stocks = self.market.list_stocks()
        self.assertIsInstance(stocks, list)
        self.assertGreater(len(stocks), 0)
        for stock in stocks:
            self.assertIsInstance(stock, Stock)

    def test_get_stock(self):
        """Test retrieving a stock by its symbol."""
        stock = self.market.get_stock("TEA")
        self.assertIsNotNone(stock)
        self.assertEqual(stock.symbol, "TEA")


if __name__ == "__main__":
    unittest.main()
