"""Module for managing the Global Beverage Corporation Exchange (GBCE) market."""

from math import prod

from stockmarket.stock.models import CommonStock, PreferredStock, Stock


class GBCE:
    """Class representing the Global Beverage Corporation Exchange (GBCE) market."""

    def __init__(self):
        """Initialize the GBCE market."""
        self.stocks = {
            "TEA": CommonStock("TEA", 0, 100),
            "POP": CommonStock("POP", 8, 100),
            "ALE": CommonStock("ALE", 23, 60),
            "GIN": PreferredStock("GIN", 8, 0.02, 100),
            "JOE": CommonStock("JOE", 13, 250),
        }

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

    def calculate_gbce_all_share_index(self) -> float:
        """Calculate the GBCE All Share Index using the geometric mean of stock prices.

        Returns
        -------
        float
            The GBCE All Share Index.
        """
        prices = [
            stock.calculate_volume_weighted_stock_price()
            for stock in self.stocks.values()
            if stock.calculate_volume_weighted_stock_price() > 0
        ]
        if not prices:
            return 0.0

        geometric_mean = prod(prices) ** (1 / len(prices))

        return geometric_mean
