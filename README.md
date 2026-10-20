# Polymarket copy-trading bot (paper money)

Copies the trades of top Polymarket traders using a **fake $1,000.00 account** and real market prices. No real money, no wallet, no keys. Runs by itself every ~10 minutes on GitHub Actions.

## Live paper trading

_Not started yet. First run is due shortly._

## Look-back test: if you had started copying 7 or 14 days ago

_Last calculated 20 Oct 2026 18:02 UTC. Copies each trade 20 min late, at a worse price (+0.01) and 1% fees._

| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |
|---|---:|---:|---:|---:|---:|
| 7 days ago | $1,000.00 | $1,587.74 | **+$587.74 (+58.8%)** | 256 | 86 / 84 |
| 14 days ago | $1,000.00 | $1,670.75 | **+$670.75 (+67.1%)** | 329 | 122 / 126 |

![backtest](data/backtest_equity.svg)

| Trader | Bets | Profit/loss (14d) |
|---|---:|---:|
| getbipped | 16 | +$395.10 |
| Tokor | 37 | +$224.27 |
| 0x2cE8505aA641791EB8460f6ac6bf5C0511E34527-1746735481513 | 8 | +$87.73 |
| Jsram | 6 | +$82.88 |
| alwaysfade | 4 | +$74.20 |
| para-Vision | 8 | +$73.77 |
| ArielFilipino | 6 | +$69.68 |
| robustmst | 2 | +$55.41 |
| jonjones1993 | 1 | +$39.50 |
| Elaran1993 | 1 | +$21.04 |
| dsasdaas | 18 | +$18.73 |
| theowalcott | 1 | +$15.20 |
| lfg100k | 3 | +$9.36 |
| ColdBlooded | 10 | +$7.57 |
| mde4life1986 | 3 | +$5.51 |
| aenews2 | 3 | +$3.92 |
| PEYZ-BIGGEST-FAN | 8 | +$3.63 |
| Siddhartha1 | 1 | +$0.35 |
| qwen4.1.fund | 1 | -$0.05 |
| balthazar | 1 | -$0.20 |
| forgotmydinner | 1 | -$0.72 |
| PiEDawg | 11 | -$1.88 |
| zerone777 | 3 | -$2.68 |
| VerilyWinningly | 7 | -$2.79 |
| wan123 | 5 | -$4.06 |
| 0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357 | 3 | -$5.22 |
| donthackme | 4 | -$6.43 |
| flawfence | 5 | -$7.30 |
| 0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495 | 24 | -$8.10 |
| SpringlyFawl | 10 | -$8.36 |
| alex20011 | 16 | -$9.32 |
| juice-fruit | 1 | -$16.78 |
| paddaa | 11 | -$17.12 |
| dromedaryy | 4 | -$21.18 |
| ic4cream | 7 | -$24.32 |
| Wiretransferxyz | 17 | -$25.99 |
| 0x448861155279dbf833d041b963e3ac854599e319 | 8 | -$44.28 |
| 0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625 | 25 | -$44.55 |
| Dragon-Evolution | 2 | -$65.22 |
| HVAB | 12 | -$97.39 |
| THEHIGHLIFE | 15 | -$103.11 |

> ⚠️ **This look-back is flattering.** Traders are picked from *today's* leaderboard, partly *because* their recent bets won. The live paper test above is the honest number - judge the strategy on that.

## Rules the bot follows

- Picks up to 60 traders on the monthly leaderboard who: made $100,000+ this month, are profitable all-time, earn at least 3% on what they trade (filters out market-making bots) and made 3+ copyable trades in the last week. Re-picks weekly.
- When one of them buys ($100+, price between 0.05 and 0.95), the bot buys $20.00 of the same outcome at the real order-book price, max $60.00 per market.
- Skips it if the price has moved more than 0.03 past what the trader paid, if the market ends within 1h, or for 5/15-minute crypto 'Up or Down' markets (impossible to copy in time).
- Sells when the trader sells. Otherwise holds until the market resolves ($1 if right, $0 if wrong).
- Assumes 1% fees on every buy and sell (conservative).

Settings live in `config.json`. Raw data: `data/live_trades.csv`, `data/live_equity.csv`, `data/backtest.json`.

_Not financial advice. Past results, especially copied ones, don't guarantee future results._
