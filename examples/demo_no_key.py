"""Keyless demo — real cross-venue order-book depth, no signup.

Runs as-is against the public DepthFeed demo endpoint (BTC 15-minute, top levels
per side). A taste of the full archive; grab a free key for every level, asset,
window and the full history: https://polymarketpricedata.com/price-data
"""

from polymarket_price_data import PolymarketPriceData


def main() -> None:
    pm = PolymarketPriceData()  # no key
    d = pm.demo()
    books = (d.get("data") or {}).get("books") or {}
    print("venues with a live book:", [v for v, b in books.items() if isinstance(b, dict)])
    for venue, b in books.items():
        if isinstance(b, dict):
            bids = b.get("bids") or b.get("yes") or []
            asks = b.get("asks") or b.get("no") or []
            print(f"  {venue:11} top bid {bids[:1]}  top ask {asks[:1]}")


if __name__ == "__main__":
    main()
