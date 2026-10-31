# Polymarket copy-trading bot (paper money)

Copies the trades of top Polymarket traders using a **fake $1,000.00 account** and real market prices. No real money, no wallet, no keys. Runs by itself every ~10 minutes on GitHub Actions.

## Head to head

| Strategy | Live account now | Live P/L | Live bets (won/finished) | Look-back 7d | Look-back 14d |
|---|---:|---:|---:|---:|---:|
| [All traders making $100k+/month (up to 60)](#wide) | $1,179.36 | +$179.36 (+17.9%) | 235 (90/171) | +$560.03 (+56%) | -$15.14 (-2%) |
| [Top 5 traders making $500k+/month](#top5) | $884.90 | -$115.10 (-11.5%) | 67 (16/34) | +$3.74 (+0%) | -$10.17 (-1%) |

<a id="wide"></a>
## All traders making $100k+/month (up to 60)

### Live paper trading (fake money, real prices)

| | |
|---|---|
| **Account value** | **$1,179.36** (started with $1,000.00) |
| **Profit / loss** | **+$179.36 (+17.9%)** |
| Running for | 10.7 days (since 20 Oct 2026 18:24 UTC) |
| Test period | until 2026-11-30 - then no new bets; open ones are held until they settle |
| Last update | 31 Oct 2026 11:22 UTC ✅ |
| Cash / in open bets | $0.00 / $1,179.36 |
| Bets opened | 235 (64 still open) |
| Finished bets won / lost | 90 / 81 (53% win rate) |

![live](data/live_wide_equity.svg)

#### Which traders are worth copying (live)

| Trader | Bets copied | Finished (won) | Profit/loss so far |
|---|---:|---:|---:|
| alwaysfade | 2 | 2 (1) | +$84.05 |
| OhWhenTheReds | 2 | 2 (2) | +$66.04 |
| 0xC9BFc7986767173b4f1c3FC9B2c6b255F | 5 | 5 (4) | +$50.86 |
| Bigggggggg | 3 | 3 (3) | +$48.75 |
| donthackme | 21 | 13 (12) | +$45.44 |
| Elaran1993 | 2 | 2 (2) | +$42.29 |
| takeormake | 7 | 7 (3) | +$37.53 |
| monkeymashingkeyboard | 2 | 2 (2) | +$35.18 |
| para-Vision | 1 | 1 (1) | +$28.58 |
| 0x448861155279dbf833d041b963e3ac854599e319 | 3 | 1 (1) | +$20.86 |
| zerone777 | 10 | 2 (1) | +$19.92 |
| 0xA0b86991c6218b36c1d19D4a29Eb0cE3606eB4 | 1 | 1 (1) | +$17.60 |
| BreakTheBank | 6 | 4 (2) | +$13.48 |
| 0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625 | 3 | 3 (2) | +$9.60 |
| Tokor | 1 | 1 (1) | +$7.20 |
| getbipped | 1 | 0 (0) | +$7.05 |
| lfg100k | 1 | 1 (1) | +$6.12 |
| paddaa | 2 | 2 (2) | +$2.30 |
| alex20011 | 16 | 7 (5) | +$1.61 |
| aenews2 | 1 | 0 (0) | +$1.15 |
| ArielFilipino | 2 | 2 (1) | +$0.42 |
| PiEDawg | 1 | 1 (0) | -$0.74 |
| THEHIGHLIFE | 1 | 1 (0) | -$1.02 |
| VerilyWinningly | 5 | 3 (1) | -$1.85 |
| SpringlyFawl | 5 | 5 (0) | -$5.74 |
| flawfence | 3 | 1 (0) | -$7.17 |
| balthazar | 16 | 12 (8) | -$8.90 |
| 0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495 | 8 | 7 (0) | -$16.83 |
| xtxpleasecallme | 1 | 1 (0) | -$17.54 |
| e46m3 | 10 | 5 (2) | -$18.54 |
| HVAB | 2 | 2 (0) | -$19.15 |
| PEYZ-BIGGEST-FAN | 5 | 5 (3) | -$19.56 |
| Mooseborzoiii | 1 | 1 (0) | -$20.20 |
| wan123 | 2 | 2 (0) | -$21.68 |
| Lucerys | 19 | 10 (6) | -$25.12 |
| Wiretransferxyz | 3 | 3 (1) | -$33.57 |
| ic4cream | 4 | 4 (1) | -$42.82 |
| qwen4.1.fund | 14 | 4 (2) | -$46.05 |
| omnibus-076daa | 43 | 43 (19) | -$60.21 |

**Currently copying 60 traders** (re-picked every 7 days, last on 27 Oct 2026 18:46 UTC): [BreakTheBank](https://polymarket.com/profile/0xf0318c32136c2db7fec88b84869aee6a1106c80c), [joseph00677](https://polymarket.com/profile/0xcdcccd0f2d86e450d973da415ad2430e5cc7935a), [e46m3](https://polymarket.com/profile/0x4f1d5ae26fc31472966e951af3183308736d8de2), [Bigggggggg](https://polymarket.com/profile/0x511f9c771449162349795d17becf8b37031acbe1), [takeormake](https://polymarket.com/profile/0xa38a455bbdd4b68486548b7e19da99903f4f821d), [juice-fruit](https://polymarket.com/profile/0x5fdd66ffd0325d4e8d1d86fbec50caa31770a747), [Abkha](https://polymarket.com/profile/0x7c75be8139d0e333e7c8c2e17b53575ef0804d1d), [balthazar](https://polymarket.com/profile/0x5a218c7ad04135830a45c41aaed7294df7809318), [eventalpha26](https://polymarket.com/profile/0x2e7bf3e7b8ba0351b737897197fd5cc34fbfbd8c), [dromedaryy](https://polymarket.com/profile/0x6575759174ad221bba9947bc3f18750ec769b198), [flawfence](https://polymarket.com/profile/0x23d81ba9371e576015c1e562db09c689f56b0288), [Jsram](https://polymarket.com/profile/0x83720820a8aa6c3f20ad71850e7a1a17d16c5223), [primm](https://polymarket.com/profile/0xd38b71f3e8ed1af71983e5c309eac3dfa9b35029), [theowalcott](https://polymarket.com/profile/0x7ad71d79a3bb90d0a87a06500fa0fe11663842aa), [monkeymashingkeyboard](https://polymarket.com/profile/0x684baa57c338c2549aec0aa3f034f695d72a8409), [THEHIGHLIFE](https://polymarket.com/profile/0x8c0b024c17831a0dde038547b7e791ae6a0d7aa5), [ArielFilipino](https://polymarket.com/profile/0xe18ecc345e00ee7c4f2d1f676f3dd2acb112f826), [Lucerys](https://polymarket.com/profile/0x1387d145aaf01f6e33b66525dda6e1f51f6955f8), [alex20011](https://polymarket.com/profile/0x4868c31e81040e002b41984842b84bae8923a1c1), [paddaa](https://polymarket.com/profile/0x60a92c8620846d81f5ea17b0564e0d4b7c545a71), [Tokor](https://polymarket.com/profile/0xa19cbababc312f9df185e49d7004c249ed1ade6b), [xtxpleasecallme](https://polymarket.com/profile/0xad5353afe30c2da57709e2704ef3ccdcf67eef24), [PEYZ-BIGGEST-FAN](https://polymarket.com/profile/0xdaef2be2a19ad331737d06545f85615b094554e9), [0x448861155279dbf833d041b963e3ac854599e319](https://polymarket.com/profile/0x448861155279dbf833d041b963e3ac854599e319), [0x9b129aD05Bc0a8df3C73DfCC66fE75252DaEC2D5-1778811687225](https://polymarket.com/profile/0x9b129ad05bc0a8df3c73dfcc66fe75252daec2d5), [para-Vision](https://polymarket.com/profile/0x676c1bb692c76b57b06f1b93817515acfa5ce139), [donthackme](https://polymarket.com/profile/0x03805a13a0b3e058f55f6c6af95389d4f431073d), [ic4cream](https://polymarket.com/profile/0x27f738fe203827445690339104aae35b20bc44b0), [0xA0b86991c6218b36c1d19D4a29Eb0cE3606eB4](https://polymarket.com/profile/0x5e6e2c3f06686f2607b86c90e35f536e81a1be00), [getbipped](https://polymarket.com/profile/0x252d7bae5ec87553dcafb23e275c202ac0d3c456), [88888x88888](https://polymarket.com/profile/0x640b954ebc87c7b68749c763d8f611c3421554b5), [mr.ozi](https://polymarket.com/profile/0x614dc8d3542c12103d2c6a3553fd761e391d1546), [Siddhartha1](https://polymarket.com/profile/0xc95ed399d2fbaec9461f2abd70e0d96df1921288), [Elaran1993](https://polymarket.com/profile/0xb7271c112cbd83eb4c1ef1b554ff963604ae2a9d), [yabanci](https://polymarket.com/profile/0x285faa3e3d1465cf3ff1bff1e1d14891f5b8495f), [defillama7](https://polymarket.com/profile/0x4c8cdcdd4c92bf44e74a642254f7414de14de36f), [0x30E4E574AF95340e873444bCa776d4D9372b8744-1770499771900](https://polymarket.com/profile/0xa2a78bb796f56b1b174b29eff72af4f0c558627b), [kaxel78](https://polymarket.com/profile/0xc1b5f266564e6d4907cf84bdf5a8f91621ef5d85), [OhWhenTheReds](https://polymarket.com/profile/0x918b42a06ff25eaaa4a79eca9da6a9de46f4ea63), [0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357](https://polymarket.com/profile/0x20d6436849f930584892730c7f96ebb2ac763856), [qwen300.fund](https://polymarket.com/profile/0xb0c85813a7a4428f1139ff91d3118a92c391fe7f), [aenews2](https://polymarket.com/profile/0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1), [ColdBlooded](https://polymarket.com/profile/0xbcc321b6336117432f4e9d2d28b20d8b6795ac9c), [rabbitfoot1](https://polymarket.com/profile/0x10a6fadcbacd66330862206f6199b197e3ad4d8b), [0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495](https://polymarket.com/profile/0xc7d02944a76b9f83b199e9090ecc92c82d241f8a), [pollo07](https://polymarket.com/profile/0x72487021e3339827c476592585c15ae7f0fa7e72), [zerone777](https://polymarket.com/profile/0xe949065b6c64308369c26dc590121623a5a4dea6), [TheReturnOfDarthMaul](https://polymarket.com/profile/0x3a8aa345d5db7ec5138298c8c4f4540259be7699), [scootergene](https://polymarket.com/profile/0xf3a6ac44c5c90ff2b4afa4459f71acc2e57971bd), [Eugycom](https://polymarket.com/profile/0x64ceab3becc143e1b97a8e16dc270c2297566015), [0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625](https://polymarket.com/profile/0x446884aa55e3dcf7123d9a3d6243c4e34b70b165), [Contestable-Parfait](https://polymarket.com/profile/0xc301c1e034e71e1a6ce9684f029c4674a00466aa), [pikachu2508](https://polymarket.com/profile/0x38891af2ad2f103ab8dc896c0243d2646deffe34), [lava-lava](https://polymarket.com/profile/0x629bc4a1e53e1d475beb7ea3d388791e96dd995a), [0xC9BFc7986767173b4f1c3FC9B2c6b255F](https://polymarket.com/profile/0xc9bfc7986767173b4f1c3fc9b2c6b255fc7381c0), [Likaseent](https://polymarket.com/profile/0x227f7ba7fcc35b7f8fc08aa6b075f5220da2a574), [Vale54holi](https://polymarket.com/profile/0x9d0dcd0c8aa0526303fd9e17fff4666ef52d2e6d), [GAMBLINGISCANCER69](https://polymarket.com/profile/0x9c56304c8840621ef4c1e707b4c7d708d09878d1), [dsasdaas](https://polymarket.com/profile/0x1e52bbdf389526f57abc62641d518868f4c5eb43), [wisewisewind](https://polymarket.com/profile/0xcdfb742c864b7011725b3b851291e326971497a0)

<details><summary>Leader trades we did <b>not</b> copy, and why</summary>

- leader trade too small / extreme price / crypto up-down: 262799
- per-market cap or out of cash: 24275
- market ends too soon: 11075
- market already closed: 325
- signal too old (run was delayed): 291
- price ran away from leader's price: 34
- order book too thin: 7

</details>

### Look-back test: if you had started copying 7 or 14 days ago

_Last calculated 31 Oct 2026 03:53 UTC. Copies each trade 20 min late, at a worse price (+0.01) and 1% fees._

| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |
|---|---:|---:|---:|---:|---:|
| 7 days ago | $1,000.00 | $1,560.03 | **+$560.03 (+56.0%)** | 339 | 126 / 138 |
| 14 days ago | $1,000.00 | $984.86 | **-$15.14 (-1.5%)** | 209 | 70 / 82 |

![backtest](data/backtest_wide_equity.svg)

| Trader | Bets | Profit/loss (14d) |
|---|---:|---:|
| drainedandpoor | 12 | +$312.23 |
| 0xC9BFc7986767173b4f1c3FC9B2c6b255F | 28 | +$174.16 |
| flawfence | 3 | +$71.49 |
| zerone777 | 5 | +$47.57 |
| paddaa | 13 | +$16.98 |
| 0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625 | 7 | +$8.22 |
| mr.ozi | 5 | +$6.37 |
| chongchong37 | 3 | +$5.89 |
| 0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357 | 1 | +$1.83 |
| 0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495 | 15 | +$1.47 |
| ic4cream | 11 | +$0.56 |
| graynotebook19 | 1 | -$1.04 |
| kaxel78 | 8 | -$4.71 |
| Vale54holi | 2 | -$5.95 |
| alex20011 | 11 | -$8.77 |
| lava-lava | 1 | -$9.99 |
| pollo07 | 7 | -$12.38 |
| dromedaryy | 2 | -$16.48 |
| Likaseent | 8 | -$17.00 |
| PEYZ-BIGGEST-FAN | 1 | -$20.20 |
| akroll | 1 | -$20.20 |
| dsasdaas | 1 | -$20.20 |
| Anjun | 9 | -$27.77 |
| getbipped | 4 | -$29.53 |
| rabbitfoot1 | 5 | -$29.96 |
| 0xf705fa045201391d9632b7f3cde06a5e24453ca7 | 10 | -$37.88 |
| para-Vision | 8 | -$40.30 |
| THEHIGHLIFE | 2 | -$46.83 |
| zb8 | 4 | -$50.45 |
| Sisyphus- | 7 | -$80.70 |
| 0x448861155279dbf833d041b963e3ac854599e319 | 14 | -$181.54 |

> ⚠️ **This look-back is flattering.** Traders are picked from *today's* leaderboard, partly *because* their recent bets won. The live paper test above is the honest number - judge the strategy on that.

<a id="top5"></a>
## Top 5 traders making $500k+/month

### Live paper trading (fake money, real prices)

| | |
|---|---|
| **Account value** | **$884.90** (started with $1,000.00) |
| **Profit / loss** | **-$115.10 (-11.5%)** |
| Running for | 10.7 days (since 20 Oct 2026 18:32 UTC) |
| Test period | until 2026-11-30 - then no new bets; open ones are held until they settle |
| Last update | 31 Oct 2026 11:23 UTC ✅ |
| Cash / in open bets | $0.00 / $884.90 |
| Bets opened | 67 (33 still open) |
| Finished bets won / lost | 16 / 18 (47% win rate) |

![live](data/live_top5_equity.svg)

#### Which traders are worth copying (live)

| Trader | Bets copied | Finished (won) | Profit/loss so far |
|---|---:|---:|---:|
| takeormake | 8 | 8 (6) | +$159.83 |
| Bigggggggg | 4 | 0 (0) | -$4.83 |
| e46m3 | 36 | 13 (7) | -$60.55 |
| BreakTheBank | 19 | 13 (3) | -$209.55 |

**Currently copying 5 traders** (re-picked every 7 days, last on 27 Oct 2026 18:48 UTC): [BreakTheBank](https://polymarket.com/profile/0xf0318c32136c2db7fec88b84869aee6a1106c80c), [joseph00677](https://polymarket.com/profile/0xcdcccd0f2d86e450d973da415ad2430e5cc7935a), [e46m3](https://polymarket.com/profile/0x4f1d5ae26fc31472966e951af3183308736d8de2), [Bigggggggg](https://polymarket.com/profile/0x511f9c771449162349795d17becf8b37031acbe1), [takeormake](https://polymarket.com/profile/0xa38a455bbdd4b68486548b7e19da99903f4f821d)

<details><summary>Leader trades we did <b>not</b> copy, and why</summary>

- leader trade too small / extreme price / crypto up-down: 25814
- market ends too soon: 3180
- per-market cap or out of cash: 2220
- market already closed: 141
- signal too old (run was delayed): 37
- price ran away from leader's price: 5
- order book too thin: 1

</details>

### Look-back test: if you had started copying 7 or 14 days ago

_Last calculated 31 Oct 2026 04:06 UTC. Copies each trade 20 min late, at a worse price (+0.01) and 1% fees._

| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |
|---|---:|---:|---:|---:|---:|
| 7 days ago | $1,000.00 | $1,003.74 | **+$3.74 (+0.4%)** | 68 | 18 / 6 |
| 14 days ago | $1,000.00 | $989.83 | **-$10.17 (-1.0%)** | 72 | 19 / 9 |

![backtest](data/backtest_top5_equity.svg)

| Trader | Bets | Profit/loss (14d) |
|---|---:|---:|
| Bigggggggg | 57 | +$75.01 |
| googleplay | 1 | +$15.20 |
| e46m3 | 5 | -$0.84 |
| joseph00677 | 4 | -$43.80 |
| BreakTheBank | 5 | -$55.74 |

> ⚠️ **This look-back is flattering.** Traders are picked from *today's* leaderboard, partly *because* their recent bets won. The live paper test above is the honest number - judge the strategy on that.

## Rules the bot follows

- Each strategy picks traders from the monthly leaderboard (All traders making $100k+/month (up to 60); Top 5 traders making $500k+/month) who are also profitable all-time, earn at least 3% on what they trade (filters out market-making bots) and made 3+ copyable trades in the last week. Re-picks weekly. Each strategy has its own separate fake account.
- When one of them buys ($100+, price between 0.05 and 0.95), the bot buys $20.00 of the same outcome at the real order-book price, max $60.00 per market.
- Skips it if the price has moved more than 0.03 past what the trader paid, if the market ends within 1h, or for 5/15-minute crypto 'Up or Down' markets (impossible to copy in time).
- Sells when the trader sells. Otherwise holds until the market resolves ($1 if right, $0 if wrong).
- Assumes 1% fees on every buy and sell (conservative).

Settings live in `config.json`. Raw data: `data/live_<strategy>_trades.csv`, `data/live_<strategy>_equity.csv`, `data/backtest_<strategy>.json`.

_Not financial advice. Past results, especially copied ones, don't guarantee future results._
