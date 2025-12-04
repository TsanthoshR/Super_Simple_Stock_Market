"""Module for managing the Global Beverage Corporation Exchange (GBCE) market."""

from math import prod

from my_logger import daily_logger
from src.stockmarket.stock.enums import TradeType
from src.stockmarket.stock.exceptions import InvalidTradeError
from src.stockmarket.stock.models import (
    CommonStock,
    NoTradeError,
    PreferredStock,
    Stock,
)


class GBCE:
    """Class representing the Global Beverage Corporation Exchange (GBCE) market."""

    def __init__(self):
        """Initialize the GBCE market."""
        self.stocks = {
            "TEA": CommonStock(symbol="TEA", last_dividend=0, par_value=100),
            "POP": CommonStock(symbol="POP", last_dividend=8, par_value=100),
            "ALE": CommonStock(symbol="ALE", last_dividend=23, par_value=60),
            "GIN": PreferredStock(
                symbol="GIN", last_dividend=8, fixed_dividend=0.02, par_value=100
            ),
            "JOE": CommonStock(symbol="JOE", last_dividend=13, par_value=250),
        }
        daily_logger.info("Initialized GBCE market with default stocks.")

    def add_Stock(self, stock: Stock) -> None:
        """Add a stock to the GBCE market.

        Parameters
        ----------
        stock : Stock
            The stock instance to be added.
        """
        self.stocks[stock.symbol] = stock

    def list_stocks(self) -> list[Stock]:
        """List all stocks in the GBCE market.

        Returns
        -------
        list[Stock]
            A list of all stock instances in the market.
        """
        return list(self.stocks.values())  # test with __repr__ method

    def get_stock(self, symbol: str) -> Stock:
        """Retrieve a stock by its symbol.

        Parameters
        ----------
        symbol : str
            The ticker symbol of the stock.

        Returns
        -------
        Stock
            The stock instance corresponding to the symbol.
        """
        return self.stocks.get(symbol)

    def record_trade(
        self, symbol: str, trade_type: TradeType, quantity: int, price: float
    ) -> None:
        """Record a trade for a given stock.

        Parameters
        ----------
        symbol : str
            The ticker symbol of the stock.
        trade_type : str
            The type of trade ('buy' or 'sell').
        quantity : int
            The quantity of shares traded.
        price : float
            The price at which the shares were traded.
        """
        if quantity <= 0:
            raise InvalidTradeError("Trade quantity must be greater than zero.")

        stock = self.get_stock(symbol)
        if stock:
            stock.record_trade(trade_type, quantity, price)
        else:
            raise KeyError(f"Stock with symbol '{symbol}' not found in the market.")

    def calculate_gbce_all_share_index(self) -> float:
        """Calculate the GBCE All Share Index using the geometric mean of stock prices.

        Returns
        -------
        float
            The GBCE All Share Index.
        """
        prices = []
        for stock in self.stocks.values():
            try:
                price = stock.calculate_volume_weighted_stock_price()
            except NoTradeError:
                # Skip stocks with no trades recorded
                continue
            if price > 0:
                prices.append(price)
        if not prices:
            return 0.0

        geometric_mean = prod(prices) ** (1 / len(prices))

        return geometric_mean
