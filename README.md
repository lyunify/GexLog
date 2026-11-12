# GexLog

Daily logger for SPY dealer gamma exposure (GEX) levels, built to support my own SPX 0DTE options trading.

## Why

Dealer gamma positioning shapes intraday price behavior. When dealers are long gamma, their hedging tends to dampen moves; when they are short gamma, hedging tends to amplify them. Key levels such as the call wall, put wall, and gamma flip often act as support, resistance, or volatility pivots.

GexLog records these levels every trading day so I can later compare them against my own trades and see whether they actually matter for my strategy.

## Key Terms

| Term | Meaning |
|---|---|
| GEX | Gamma exposure: total gamma held by options dealers across all open contracts |
| Call wall | Strike with the largest call gamma; often acts as resistance |
| Put wall | Strike with the largest put gamma; often acts as support |
| Gamma flip | Price where net GEX turns from positive to negative |
| Regime | `positive_gamma` (calmer markets) or `negative_gamma` (more volatile markets) |

## How It Works (v1)

1. `fetch_levels.py` calls the FlashAlpha summary endpoint for SPY.
2. The raw response is saved as JSON for development and testing.
3. *(In progress)* Selected fields are appended to a daily CSV.
4. *(Planned)* The script runs automatically every trading day.

## Setup

```bash
git clone https://github.com/lyunify/GexLog.git
cd GexLog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python fetch_levels.py
```

## Data Source and Limitations

- Data comes from [FlashAlpha](https://flashalpha.com) via the public `/v1/stock/{symbol}/summary` endpoint, which does not require an API key.
- FlashAlpha's free tier does not include index or ETF data on its key-levels endpoint, so v1 uses the summary endpoint for SPY.
- SPY is used as a proxy for SPX. Multiplying SPY levels by about 10 gives a rough SPX equivalent, but the two have different options positioning, so the mapping is approximate.

## Roadmap

- [x] Fetch SPY GEX summary from FlashAlpha
- [ ] Parse key fields and append to CSV
- [ ] Schedule daily runs
- [ ] Compare logged levels with my own trade history
- [ ] v2: compute SPX GEX directly from Schwab option chain data

## Disclaimer

This is a personal learning project, not financial advice.
