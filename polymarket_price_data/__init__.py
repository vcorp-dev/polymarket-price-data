"""
polymarket_price_data — Polymarket prediction-market PRICE DATA through the
DepthFeed aggregator: live 0–1 prices, full order-book depth, and the history
the public API can't back-fill — Polymarket, Kalshi and Limitless in one API.

"Price data" = the prediction-market contract price (each outcome quoted 0..1
= implied probability), NOT the $POLY token.

Get a free key + docs: https://depthfeed.com/price-data
"""

from .client import PolymarketPriceData

__all__ = ["PolymarketPriceData"]
__version__ = "1.0.0"
