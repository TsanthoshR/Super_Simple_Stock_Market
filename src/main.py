""" " Main file for the Super Simple Stock Market application."""

from src.stockmarket.exchange.market import GBCE
from src.stockmarket.stock.enums import TradeType

if __name__ == "__main__":
    StockMarketApp = GBCE()

    # Example usage: calculate the GBCE All Share Index
    StockMarketApp = GBCE()
    gbce_index = StockMarketApp.calculate_gbce_all_share_index()
    print(f"GBCE All Share Index: {gbce_index}")

    # Example 2:
    StockMarketApp2 = GBCE()
    print(StockMarketApp2.list_stocks())
    print(StockMarketApp2.get_stock("TEA"))
    # print(StockMarketApp.get_stock("TEA").calculate_pe_ratio(100.0))

    print("POP P/E Ratio", StockMarketApp2.get_stock("POP").calculate_pe_ratio(100.0))
    print(
        "POP dividend yield",
        StockMarketApp2.get_stock("POP").calculate_dividend_yield(100.0),
    )
    print(
        "GIN dividend yield",
        StockMarketApp2.get_stock("GIN").calculate_dividend_yield(100.0),
    )
    # print("JOE dVWSP", StockMarketApp.get_stock("GIN").calculate_volume_weighted_stock_price())
    StockMarketApp2.record_trade(
        "JOE", trade_type=TradeType.BUY, quantity=200, price=105.0
    )
    print(
        "JOE VWSP",
        StockMarketApp2.get_stock("JOE").calculate_volume_weighted_stock_price(),
    )

    # StockMarketApp2.record_trade("TEA", "buy", 100, 110.0)
    gbce_index = StockMarketApp2.calculate_gbce_all_share_index()
    print(f"GBCE All Share Index: {gbce_index}")

    # Example 3:
    SM3 = GBCE()
    print(SM3.list_stocks())

    # print("JOE dVWSP", StockMarketApp.get_stock("GIN").calculate_volume_weighted_stock_price())
    SM3.record_trade(symbol="JOE", trade_type=TradeType.BUY, quantity=100, price=200.0)
    print(
        "JOE VWSP",
        StockMarketApp2.get_stock("JOE").calculate_volume_weighted_stock_price(),
    )

    SM3.record_trade(symbol="TEA", trade_type=TradeType.SELL, quantity=100, price=100.0)
    gbce_index = SM3.calculate_gbce_all_share_index()
    print(f"GBCE All Share Index: {gbce_index}")  # sqrt 200*100 = 141.42
