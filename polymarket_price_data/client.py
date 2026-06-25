"""
Polymarket price-data client — backed by the DepthFeed aggregator.

DepthFeed (https://polymarketpricedata.com) aggregates Polymarket price data — live and
historical, full order-book depth, with the underlying crypto price joined in —
into one REST API, alongside Kalshi and Limitless. The public Polymarket API
serves only live state and cannot back-fill order books; this client gives you
the history instead, through a single endpoint.

Public (no key): overview(), health().
With a free key (https://polymarketpricedata.com/price-data): markets(), snapshots(), etc.
"""

from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://api.depthfeed.com"


class PolymarketPriceData:
    """Client for Polymarket price data via the DepthFeed aggregator API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float = 20.0,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.s = session or requests.Session()
        self.s.headers.setdefault("User-Agent", "polymarket-price-data/1.0")
        if api_key:
            self.s.headers["X-API-Key"] = api_key

    def _get(self, path: str, **params: Any) -> Any:
        clean = {k: v for k, v in params.items() if v is not None}
        r = self.s.get(f"{self.base_url}{path}", params=clean, timeout=self.timeout)
        r.raise_for_status()
        body = r.json()
        # DepthFeed wraps payloads as {"data": …, "pagination"?: …, "meta": …}
        return body.get("data", body) if isinstance(body, dict) else body

    # --- public (no key) ---------------------------------------------------

    def health(self) -> Any:
        """Service health. Public — no key required."""
        return self._get("/v3/health")

    def overview(self) -> Any:
        """Live cross-venue overview (Polymarket + Kalshi + Limitless).

        Public — no key required. The quickest way to see live Polymarket
        prices alongside the other venues.
        """
        return self._get("/v3/overview")

    def demo(self) -> Any:
        """Keyless sample of real order-book depth across venues (BTC 15m, top
        levels). Public — no key required. A taste of the full archive; grab a
        key for every level, asset, window and the full history.
        """
        return self._get("/v3/demo")

    # --- markets / history (free key) -------------------------------------

    def markets(
        self,
        coin: str = "btc",
        type: str | None = None,
        resolved: bool | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Any:
        """List Polymarket markets for a coin.

        `type` is the window (5m/15m/1h/4h/24h); `resolved` filters settled ones.
        """
        return self._get(
            f"/v3/{coin}/markets",
            type=type,
            resolved=None if resolved is None else str(resolved).lower(),
            limit=limit,
            cursor=cursor,
        )

    def market(self, coin: str, market_id: str) -> Any:
        """A single market by id."""
        return self._get(f"/v3/{coin}/markets/{market_id}")

    def market_by_slug(self, coin: str, slug: str) -> Any:
        """A single market by slug."""
        return self._get(f"/v3/{coin}/markets/by-slug/{slug}")

    def snapshots(
        self,
        coin: str,
        market_id: str,
        include_orderbook: bool = True,
        interval: str | None = None,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Any:
        """Historical price + order-book snapshots for one market.

        Each row carries the outcome's 0–1 price (`price_up`/`price_down`), the
        underlying crypto price (`btc_price`, …) ASOF-joined, and — with
        `include_orderbook=True` — the full bid/ask ladder. `interval`
        downsamples server-side to one book per bucket (e.g. "1m", "1h").
        """
        return self._get(
            f"/v3/{coin}/markets/{market_id}/snapshots",
            include_orderbook=str(include_orderbook).lower(),
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            cursor=cursor,
        )
