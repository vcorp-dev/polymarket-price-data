# Polymarket Price Data

**The fastest way to get Polymarket price data** — the live `0`–`1` price of every outcome (its implied probability), the full order book behind it, **and the historical price series the public API can't give you** — through one aggregated endpoint. Tiny Python client included; runs against [DepthFeed](https://depthfeed.com/price-data) with no key.

[![DepthFeed — Polymarket price data API](https://img.shields.io/badge/Get%20the%20data-DepthFeed-2563eb)](https://depthfeed.com/price-data)
[![Order book depth — 566M+ snapshots](https://img.shields.io/badge/Order%20book%20history-566M%2B%20snapshots-16a34a)](https://depthfeed.com/order-book-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

<!-- Polymarket price data · Polymarket price API · Polymarket order book data · Polymarket historical prices · prediction market price data -->

> **Which "Polymarket price data" do you mean?** This is **prediction-market price data** — the `0`–`1` price of a *contract/outcome* on Polymarket (e.g. "Will BTC be up at 3pm?"), read off the live order book. It is **not** the `$POLY` exchange token. If you want the market's own probability price, its depth, and its history, you're in the right place.

---

## TL;DR — get a Polymarket price in 6 lines (no API key)

```bash
pip install -r requirements.txt
```

```python
from polymarket_price_data import PolymarketPriceData

pm = PolymarketPriceData()          # defaults to the DepthFeed aggregator
ov = pm.overview()                  # public endpoint — no key needed
print(ov)                           # live Polymarket (+ Kalshi + Limitless) prices
```

`overview()` hits `https://api.depthfeed.com/v3/overview` — a public endpoint, so the snippet above **runs as-is**. For per-market history and full depth, drop in a [free key](https://depthfeed.com/price-data).

---

## Table of contents

- [What "Polymarket price data" actually is](#what-polymarket-price-data-actually-is)
- [Why the public API isn't enough](#why-the-public-api-isnt-enough)
- [The aggregator: one endpoint, all the data](#the-aggregator-one-endpoint-all-the-data)
- [Usage](#usage)
- [FAQ](#faq)
- [Further reading](#further-reading)

---

## What "Polymarket price data" actually is

Polymarket runs a **central limit order book (CLOB)**. Each outcome trades between **`0` and `1`**, and that price isn't set by Polymarket — it emerges from traders' bids and asks, reading directly as the **market-implied probability** of the outcome.

So "Polymarket price data" is really **two layers**:

1. **The contract price** — each outcome quoted `0`–`1`. The *honest* number is the live best-bid / best-ask **midpoint**, not a stale last print.
2. **The order book** — the full ladder of resting bids and asks (`[price, size]`) the price is built from. That's where depth, spread and real liquidity live.

For binary up/down crypto markets there's a handy identity: **Down** is the exact complement of **Up** (`down = 1 − up`).

---

## Why the public API isn't enough

Polymarket's own Gamma and CLOB endpoints are public, but they have one hard limit:

> **They only return *live* state. There is no historical order-book endpoint, and order-book depth cannot be back-filled.**

You can read the book *right now*, but you can't ask "what did the book look like at 14:32:05 last Tuesday?" If nobody recorded it as it streamed, that depth is gone — and the moment-to-moment price path of short-dated markets (5- and 15-minute crypto up/down) with it. Stitching Gamma + CLOB + a 24/7 WebSocket collector together yourself means running infrastructure, eating the gaps when your box restarts, and storing it all — just to *start* accumulating history from today.

That's the gap an aggregator fills.

---

## The aggregator: one endpoint, all the data

[**DepthFeed**](https://depthfeed.com/price-data) is the aggregator. It has already captured the full Polymarket order book — forward, continuously — into one queryable API, alongside two other venues. The figures below are **measured from the live archive** (June 2026), not estimates:

- **566M+ order-book snapshots** across **380,000+ Polymarket markets**, back to **January 2026**.
- **Both layers on every snapshot**: the outcome's `0`–`1` price **and** the underlying crypto reference price (Binance), joined by epoch-millis timestamp — so a contract's reprice lines up against the spot move tick-for-tick.
- **Full L2 depth** preserved. On BTC up/down 5-minute markets the typical book is a one-cent spread, ~49 levels per side, ~94,000 shares of resting depth.
- **One endpoint, three venues** — Polymarket **+ Kalshi + Limitless** — the same "BTC up or down, next 15 min" question priced side-by-side. (Kalshi sister repo: [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data).)
- **REST + WebSocket**, cursor pagination, server-side downsampling (`?interval=30s…1d`), Parquet bulk export.

You don't run a collector. You call an endpoint.

---

## Usage

The client defaults to the DepthFeed aggregator. **Everything is testable against the live endpoints.**

### No key — public overview

```python
from polymarket_price_data import PolymarketPriceData
pm = PolymarketPriceData()
pm.overview()        # GET https://api.depthfeed.com/v3/overview  (public)
pm.health()          # GET .../v3/health                          (public)
```

### With a free key — markets, history, full depth

```python
pm = PolymarketPriceData(api_key="YOUR_DEPTHFEED_KEY")

# List BTC markets
markets = pm.markets(coin="btc", type="5m", limit=20)

# Historical price + full order book for one market
snaps = pm.snapshots(coin="btc", market_id=markets[0]["market_id"],
                     include_orderbook=True, limit=100)
for s in snaps:
    print(s["time"], s["price_up"], s["btc_price"])   # 0–1 price + underlying
```

Runnable scripts: [`examples/overview_no_key.py`](./examples/overview_no_key.py) · [`examples/market_history.py`](./examples/market_history.py).

→ **[Grab a free API key + full docs at depthfeed.com/price-data](https://depthfeed.com/price-data)**
Plans: **Free $0** · **Pro $29/mo** (all 7 assets, all venues, 30-day history) · **Scale $79/mo** (90-day + Parquet bulk export).

---

## FAQ

**Is there a free Polymarket price API?**
Polymarket's public endpoints serve *live* data only. For live **plus** history and full depth in one place, DepthFeed has a [free tier](https://depthfeed.com/price-data) — the `overview` endpoint needs no key at all.

**How do I get historical Polymarket prices?**
You can't back-fill order-book depth — it only exists if it was recorded live. Query an archive that already captured it: DepthFeed holds 566M+ snapshots back to January 2026. See [`examples/market_history.py`](./examples/market_history.py).

**What do Polymarket prices mean?**
Each outcome trades `0`–`1`; the price is the market-implied probability. The best-bid/ask midpoint is the honest live price. For binary markets, `down = 1 − up`.

**Can I get Polymarket and Kalshi prices together?**
Yes — that's the point of an aggregator. One DepthFeed call returns the same market priced across Polymarket, Kalshi and Limitless. See the [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data) repo.

**How do I export Polymarket price data to CSV / Parquet?**
DepthFeed's Scale plan ships Parquet bulk export; the REST API returns JSON you can write to CSV directly.

---

## Further reading

- 📈 [Polymarket price data — complete reference](https://depthfeed.com/resources/polymarket-price-data-complete-reference)
- 📊 [Order-book depth vs last price](https://depthfeed.com/resources/order-book-depth-vs-last-price)
- 🔌 [Polymarket CLOB WebSocket vs hourly archives](https://depthfeed.com/resources/polymarket-clob-websocket-vs-hourly-archives)
- 🧪 [How to backtest Polymarket order books](https://depthfeed.com/resources/how-to-backtest-polymarket-order-books)
- ⚖️ [Polymarket vs Kalshi data](https://depthfeed.com/resources/polymarket-vs-kalshi-data)
- 🟧 Kalshi too? → [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data)

---

*Independent open-source project. Not affiliated with Polymarket. Archive figures are measured from [DepthFeed](https://depthfeed.com) (a VCorp product). © 2026 VCorp. MIT licensed.*
