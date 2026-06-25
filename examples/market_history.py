"""Historical Polymarket price + full order book for one market.

Needs a free DepthFeed key: https://polymarketpricedata.com/price-data
    export DEPTHFEED_API_KEY=...
"""

import os

from polymarket_price_data import PolymarketPriceData


def main() -> None:
    key = os.environ.get("DEPTHFEED_API_KEY")
    if not key:
        raise SystemExit("Set DEPTHFEED_API_KEY (free at https://polymarketpricedata.com/price-data)")

    pm = PolymarketPriceData(api_key=key)

    markets = pm.markets(coin="btc", type="5m", limit=1)
    market_id = markets[0]["market_id"]
    print("market:", markets[0].get("slug"), market_id)

    snaps = pm.snapshots(coin="btc", market_id=market_id,
                         include_orderbook=True, limit=5)
    for s in snaps:
        print(f"{s['time']}  up={s['price_up']}  btc={s.get('btc_price')}")
        ob = s.get("orderbook_up", {})
        print("   best bid:", (ob.get("bids") or [None])[0],
              " best ask:", (ob.get("asks") or [None])[0])


if __name__ == "__main__":
    main()
