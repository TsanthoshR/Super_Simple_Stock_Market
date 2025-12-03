"""Exceptions for stock market database operations."""


class InvalistStockError(Exception):
    """Exception raised for invalid stock operations."""

    pass


class InvalidTradeError(Exception):
    """Exception raised for invalid trade operations."""

    pass
