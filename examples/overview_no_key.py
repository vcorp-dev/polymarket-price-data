"""Live Polymarket (+ Kalshi + Limitless) prices — public endpoint, no API key.

Runs as-is against the DepthFeed aggregator.
"""

from polymarket_price_data import PolymarketPriceData


def main() -> None:
    pm = PolymarketPriceData()  # no key needed for the overview
    print("health:", pm.health())
    print("\noverview (live cross-venue prices):")
    print(pm.overview())


if __name__ == "__main__":
    main()
