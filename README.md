# Polymarket copy-trading bot (paper money)

Copies the trades of top Polymarket traders using a **fake $1,000.00 account** and real market prices. No real money, no wallet, no keys. Runs by itself every ~10 minutes on GitHub Actions.

## Live paper trading

_Not started yet. First run is due shortly._

## Look-back test

_Running... results will appear here._

## Rules the bot follows

- Picks the top 15 traders on the monthly leaderboard who: made $10,000+ this month, are profitable all-time, earn at least 3% on what they trade (filters out market-making bots) and made 3+ copyable trades in the last week. Re-picks weekly.
- When one of them buys ($100+, price between 0.05 and 0.95), the bot buys $20.00 of the same outcome at the real order-book price, max $60.00 per market.
- Skips it if the price has moved more than 0.03 past what the trader paid, if the market ends within 1h, or for 5/15-minute crypto 'Up or Down' markets (impossible to copy in time).
- Sells when the trader sells. Otherwise holds until the market resolves ($1 if right, $0 if wrong).
- Assumes 1% fees on every buy and sell (conservative).

Settings live in `config.json`. Raw data: `data/live_trades.csv`, `data/live_equity.csv`, `data/backtest.json`.

_Not financial advice. Past results, especially copied ones, don't guarantee future results._
