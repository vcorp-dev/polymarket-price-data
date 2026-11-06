# Polymarket Price Data

**The fastest way to get Polymarket historical data and live price data** — the `0`–`1` price of every outcome, the full order book behind it, and a replayable historical series — through one aggregated API. This small Python client runs against [DepthFeed](https://depthfeed.com) and includes a keyless live overview.

[![DepthFeed — Polymarket price data API](https://img.shields.io/badge/Get%20the%20data-DepthFeed-2563eb)](https://polymarketpricedata.com/price-data)
[![Order book depth — 566M+ snapshots](https://img.shields.io/badge/Order%20book%20history-566M%2B%20snapshots-16a34a)](https://polymarketpricedata.com/order-book-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

<!-- Polymarket price data · Polymarket price API · Polymarket order book data · Polymarket historical prices · prediction market price data -->

> **Which "Polymarket price data" do you mean?** This is **prediction-market price data** — the `0`–`1` price of a *contract/outcome* on Polymarket (e.g. "Will BTC be up at 3pm?"), read off the live order book. It is **not** the `$POLY` exchange token. If you want the market's own probability price, its depth, and its history, you're in the right place.

---

## Installation and quickstart — get a Polymarket price in 6 lines

```bash
pip install -r requirements.txt
```

```python
from polymarket_price_data import PolymarketPriceData

pm = PolymarketPriceData()          # defaults to the DepthFeed aggregator
ov = pm.overview()                  # public endpoint — no key needed
print(ov)                           # live Polymarket (+ Kalshi + Limitless) prices
```

`overview()` hits `https://api.depthfeed.com/v3/overview` — a public endpoint, so the snippet above **runs as-is**. For per-market history and full depth, drop in a [free key](https://polymarketpricedata.com/price-data).

---

## Table of contents

- [What "Polymarket price data" actually is](#what-polymarket-price-data-actually-is)
- [Why the public API isn't enough](#why-the-public-api-isnt-enough)
- [Live proof and data coverage](#live-proof-and-data-coverage)
- [Usage examples](#usage-examples)
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

## Live proof and data coverage

[**DepthFeed**](https://polymarketpricedata.com/price-data) is the aggregator. It has already captured the full Polymarket order book — forward, continuously — into one queryable API, alongside two other venues. The figures below are **measured from the live archive** (June 2026), not estimates:

- **566M+ order-book snapshots** across **380,000+ Polymarket markets**, back to **January 2026**.
- **Both layers on every snapshot**: the outcome's `0`–`1` price **and** the underlying crypto reference price (Binance), joined by epoch-millis timestamp — so a contract's reprice lines up against the spot move tick-for-tick.
- **Full L2 depth** preserved. On BTC up/down 5-minute markets the typical book is a one-cent spread, ~49 levels per side, ~94,000 shares of resting depth.
- **One endpoint, three venues** — Polymarket **+ Kalshi + Limitless** — the same "BTC up or down, next 15 min" question priced side-by-side. (Kalshi sister repo: [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data).)
- **REST + WebSocket**, cursor pagination, server-side downsampling (`?interval=30s…1d`), Parquet bulk export.

You don't run a collector. You call an endpoint.

---

## Usage examples

The client defaults to the DepthFeed aggregator. **Everything is testable against the live endpoints.**

### No key — try real data instantly

```python
from polymarket_price_data import PolymarketPriceData
pm = PolymarketPriceData()
pm.overview()        # GET /v3/overview  (public) — live cross-venue prices
pm.health()          # GET /v3/health    (public)
```

`overview()` returns live cross-venue market prices with no signup. It is the fastest way to verify connectivity before adding an API key for historical snapshots and full depth.

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

Full endpoint reference: **[polymarketpricedata.com/docs](https://polymarketpricedata.com/docs)** · [API overview](https://polymarketpricedata.com/data-api).

→ **[Grab a free API key at polymarketpricedata.com/price-data](https://polymarketpricedata.com/price-data)**
See [current DepthFeed plans and limits](https://depthfeed.com/pricing). Check `/v3/whoami` for your account's effective access.

---

## FAQ

**Is there a free Polymarket price API?**
Polymarket's public endpoints serve *live* data only. For live **plus** history and full depth in one place, DepthFeed has a [free tier](https://polymarketpricedata.com/price-data) — the `overview` endpoint needs no key at all.

**How do I get historical Polymarket prices?**
You can't back-fill order-book depth — it only exists if it was recorded live. Query an archive that already captured it: DepthFeed holds 566M+ snapshots back to January 2026. See [`examples/market_history.py`](./examples/market_history.py).

**What do Polymarket prices mean?**
Each outcome trades `0`–`1`; the price is the market-implied probability. The best-bid/ask midpoint is the honest live price. For binary markets, `down = 1 − up`.

**Can I get Polymarket and Kalshi prices together?**
Yes — that's the point of an aggregator. One DepthFeed call returns the same market priced across Polymarket, Kalshi and Limitless. See the [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data) repo.

**How do I export Polymarket price data to CSV / Parquet?**
For Parquet delivery, see [bulk data options](https://depthfeed.com/bulk-data). REST responses are JSON you can write to CSV.

---

## Further reading

- 🔌 [Official DepthFeed Polymarket API guide](https://depthfeed.com/resources/polymarket-api-guide)
- 🧪 [Prediction-market trading bot backtesting](https://depthfeed.com/resources/prediction-market-trading-bot-backtesting)
- 🧪 [Paper trade Polymarket strategies on live displayed books](https://depthfeed.com/polymarket-paper-trading)
- 📈 [Polymarket price data — complete reference](https://polymarketpricedata.com/resources/polymarket-price-data-complete-reference)
- 📊 [Order-book depth vs last price](https://polymarketpricedata.com/resources/order-book-depth-vs-last-price)
- 🔌 [Polymarket CLOB WebSocket vs hourly archives](https://polymarketpricedata.com/resources/polymarket-clob-websocket-vs-hourly-archives)
- 🧪 [How to backtest Polymarket order books](https://polymarketpricedata.com/resources/how-to-backtest-polymarket-order-books)
- ⚖️ [Polymarket vs Kalshi data](https://polymarketpricedata.com/resources/polymarket-vs-kalshi-data)
- 🟧 Kalshi too? → [**kalshi-price-data**](https://github.com/vcorp-dev/kalshi-price-data)

---

Contributions are welcome; see [CONTRIBUTING.md](./CONTRIBUTING.md). For product help, use [DepthFeed support](https://depthfeed.com/contact). Report vulnerabilities privately through [SECURITY.md](./SECURITY.md).

*Independent open-source project. Not affiliated with Polymarket. Archive figures are measured from [DepthFeed](https://depthfeed.com) (a VCorp product). © 2026 VCorp. MIT licensed.*
