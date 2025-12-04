"""Extra unit tests for GBCE market operations."""

import unittest

from src.stockmarket.exchange.market import GBCE
from src.stockmarket.stock.exceptions import InvalidTradeError
from src.stockmarket.stock.models import CommonStock


class TestGBCEExtra(unittest.TestCase):
    """Extra unit tests for GBCE market operations."""

    def setUp(self):
        self.market = GBCE()

    def test_record_trade_nonexistent_raises_keyerror(self):
        """Test that recording a trade for a non-existent stock raises KeyError."""
        with self.assertRaises(KeyError):
            self.market.record_trade(
                symbol="NOPE", trade_type="BUY", quantity=10, price=50.0
            )

    def test_record_trade_invalid_quantity_raises_InvalidTradeError(self):
        """Test that recording a trade with invalid quantity raises
        InvalidTradeError."""
        with self.assertRaises(InvalidTradeError):
            self.market.record_trade(
                symbol="TEA", trade_type="BUY", quantity=-1, price=10.0
            )

    def test_gbce_geometric_mean_with_multiple_prices(self):
        """Test GBCE All Share Index calculation with multiple stock prices."""
        # Record trades for two stocks so GBCE geometric mean is computed
        self.market.record_trade(
            symbol="TEA", trade_type="BUY", quantity=10, price=100.0
        )
        self.market.record_trade(symbol="POP", trade_type="BUY", quantity=5, price=25.0)

        gbce_index = self.market.calculate_gbce_all_share_index()
        expected = (100.0 * 25.0) ** 0.5  # geometric mean of the two prices
        self.assertAlmostEqual(gbce_index, expected)

    def test_add_and_get_stock(self):
        """Test adding and retrieving a stock from the market._"""
        new = CommonStock(symbol="XTEST", last_dividend=1.0, par_value=10.0)
        self.market.add_Stock(new)
        found = self.market.get_stock("XTEST")
        self.assertIsNotNone(found)
        self.assertEqual(found.symbol, "XTEST")


if __name__ == "__main__":
    unittest.main()
