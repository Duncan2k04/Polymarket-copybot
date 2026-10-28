# Polymarket copy-trading bot (paper money)

Copies the trades of top Polymarket traders using a **fake $1,000.00 account** and real market prices. No real money, no wallet, no keys. Runs by itself every ~10 minutes on GitHub Actions.

## Head to head

| Strategy | Live account now | Live P/L | Live bets (won/finished) | Look-back 7d | Look-back 14d |
|---|---:|---:|---:|---:|---:|
| [All traders making $100k+/month (up to 60)](#wide) | $1,186.21 | +$186.21 (+18.6%) | 215 (78/151) | +$202.03 (+20%) | +$68.29 (+7%) |
| [Top 5 traders making $500k+/month](#top5) | $791.39 | -$208.61 (-20.9%) | 47 (7/19) | +$173.28 (+17%) | +$69.47 (+7%) |

<a id="wide"></a>
## All traders making $100k+/month (up to 60)

### Live paper trading (fake money, real prices)

| | |
|---|---|
| **Account value** | **$1,186.21** (started with $1,000.00) |
| **Profit / loss** | **+$186.21 (+18.6%)** |
| Running for | 7.4 days (since 20 Oct 2026 18:24 UTC) |
| Test period | until 2026-11-30 - then no new bets; open ones are held until they settle |
| Last update | 28 Oct 2026 03:49 UTC ✅ |
| Cash / in open bets | $0.00 / $1,186.21 |
| Bets opened | 215 (64 still open) |
| Finished bets won / lost | 78 / 73 (52% win rate) |

![live](data/live_wide_equity.svg)

#### Which traders are worth copying (live)

| Trader | Bets copied | Finished (won) | Profit/loss so far |
|---|---:|---:|---:|
| alwaysfade | 2 | 2 (1) | +$84.05 |
| OhWhenTheReds | 2 | 2 (2) | +$66.04 |
| Bigggggggg | 3 | 3 (3) | +$48.75 |
| donthackme | 20 | 12 (11) | +$47.03 |
| Elaran1993 | 2 | 2 (2) | +$42.29 |
| takeormake | 7 | 7 (3) | +$37.53 |
| BreakTheBank | 6 | 4 (2) | +$32.00 |
| para-Vision | 1 | 1 (1) | +$28.58 |
| zerone777 | 10 | 2 (1) | +$22.24 |
| 0x448861155279dbf833d041b963e3ac854599e319 | 3 | 1 (1) | +$18.00 |
| 0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625 | 3 | 3 (2) | +$9.60 |
| Tokor | 1 | 1 (1) | +$7.20 |
| e46m3 | 9 | 4 (2) | +$6.66 |
| lfg100k | 1 | 1 (1) | +$6.12 |
| paddaa | 2 | 2 (2) | +$2.30 |
| ArielFilipino | 2 | 2 (1) | +$0.42 |
| alex20011 | 15 | 6 (4) | -$0.04 |
| PiEDawg | 1 | 1 (0) | -$0.74 |
| aenews2 | 1 | 0 (0) | -$0.88 |
| THEHIGHLIFE | 1 | 1 (0) | -$1.02 |
| 0xC9BFc7986767173b4f1c3FC9B2c6b255F | 3 | 0 (0) | -$1.25 |
| VerilyWinningly | 4 | 3 (1) | -$1.91 |
| SpringlyFawl | 5 | 5 (0) | -$5.74 |
| flawfence | 3 | 1 (0) | -$5.99 |
| balthazar | 15 | 11 (7) | -$7.34 |
| PEYZ-BIGGEST-FAN | 4 | 4 (3) | -$7.59 |
| wan123 | 2 | 1 (0) | -$14.68 |
| 0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495 | 8 | 7 (0) | -$16.78 |
| HVAB | 2 | 2 (0) | -$19.15 |
| Mooseborzoiii | 1 | 1 (0) | -$20.20 |
| omnibus-076daa | 41 | 38 (17) | -$23.31 |
| Lucerys | 14 | 10 (6) | -$23.83 |
| Wiretransferxyz | 3 | 3 (1) | -$33.57 |
| ic4cream | 4 | 4 (1) | -$42.82 |
| qwen4.1.fund | 14 | 4 (2) | -$45.75 |

**Currently copying 60 traders** (re-picked every 7 days, last on 27 Oct 2026 18:46 UTC): [BreakTheBank](https://polymarket.com/profile/0xf0318c32136c2db7fec88b84869aee6a1106c80c), [joseph00677](https://polymarket.com/profile/0xcdcccd0f2d86e450d973da415ad2430e5cc7935a), [e46m3](https://polymarket.com/profile/0x4f1d5ae26fc31472966e951af3183308736d8de2), [Bigggggggg](https://polymarket.com/profile/0x511f9c771449162349795d17becf8b37031acbe1), [takeormake](https://polymarket.com/profile/0xa38a455bbdd4b68486548b7e19da99903f4f821d), [juice-fruit](https://polymarket.com/profile/0x5fdd66ffd0325d4e8d1d86fbec50caa31770a747), [Abkha](https://polymarket.com/profile/0x7c75be8139d0e333e7c8c2e17b53575ef0804d1d), [balthazar](https://polymarket.com/profile/0x5a218c7ad04135830a45c41aaed7294df7809318), [eventalpha26](https://polymarket.com/profile/0x2e7bf3e7b8ba0351b737897197fd5cc34fbfbd8c), [dromedaryy](https://polymarket.com/profile/0x6575759174ad221bba9947bc3f18750ec769b198), [flawfence](https://polymarket.com/profile/0x23d81ba9371e576015c1e562db09c689f56b0288), [Jsram](https://polymarket.com/profile/0x83720820a8aa6c3f20ad71850e7a1a17d16c5223), [primm](https://polymarket.com/profile/0xd38b71f3e8ed1af71983e5c309eac3dfa9b35029), [theowalcott](https://polymarket.com/profile/0x7ad71d79a3bb90d0a87a06500fa0fe11663842aa), [monkeymashingkeyboard](https://polymarket.com/profile/0x684baa57c338c2549aec0aa3f034f695d72a8409), [THEHIGHLIFE](https://polymarket.com/profile/0x8c0b024c17831a0dde038547b7e791ae6a0d7aa5), [ArielFilipino](https://polymarket.com/profile/0xe18ecc345e00ee7c4f2d1f676f3dd2acb112f826), [Lucerys](https://polymarket.com/profile/0x1387d145aaf01f6e33b66525dda6e1f51f6955f8), [alex20011](https://polymarket.com/profile/0x4868c31e81040e002b41984842b84bae8923a1c1), [paddaa](https://polymarket.com/profile/0x60a92c8620846d81f5ea17b0564e0d4b7c545a71), [Tokor](https://polymarket.com/profile/0xa19cbababc312f9df185e49d7004c249ed1ade6b), [xtxpleasecallme](https://polymarket.com/profile/0xad5353afe30c2da57709e2704ef3ccdcf67eef24), [PEYZ-BIGGEST-FAN](https://polymarket.com/profile/0xdaef2be2a19ad331737d06545f85615b094554e9), [0x448861155279dbf833d041b963e3ac854599e319](https://polymarket.com/profile/0x448861155279dbf833d041b963e3ac854599e319), [0x9b129aD05Bc0a8df3C73DfCC66fE75252DaEC2D5-1778811687225](https://polymarket.com/profile/0x9b129ad05bc0a8df3c73dfcc66fe75252daec2d5), [para-Vision](https://polymarket.com/profile/0x676c1bb692c76b57b06f1b93817515acfa5ce139), [donthackme](https://polymarket.com/profile/0x03805a13a0b3e058f55f6c6af95389d4f431073d), [ic4cream](https://polymarket.com/profile/0x27f738fe203827445690339104aae35b20bc44b0), [0xA0b86991c6218b36c1d19D4a29Eb0cE3606eB4](https://polymarket.com/profile/0x5e6e2c3f06686f2607b86c90e35f536e81a1be00), [getbipped](https://polymarket.com/profile/0x252d7bae5ec87553dcafb23e275c202ac0d3c456), [88888x88888](https://polymarket.com/profile/0x640b954ebc87c7b68749c763d8f611c3421554b5), [mr.ozi](https://polymarket.com/profile/0x614dc8d3542c12103d2c6a3553fd761e391d1546), [Siddhartha1](https://polymarket.com/profile/0xc95ed399d2fbaec9461f2abd70e0d96df1921288), [Elaran1993](https://polymarket.com/profile/0xb7271c112cbd83eb4c1ef1b554ff963604ae2a9d), [yabanci](https://polymarket.com/profile/0x285faa3e3d1465cf3ff1bff1e1d14891f5b8495f), [defillama7](https://polymarket.com/profile/0x4c8cdcdd4c92bf44e74a642254f7414de14de36f), [0x30E4E574AF95340e873444bCa776d4D9372b8744-1770499771900](https://polymarket.com/profile/0xa2a78bb796f56b1b174b29eff72af4f0c558627b), [kaxel78](https://polymarket.com/profile/0xc1b5f266564e6d4907cf84bdf5a8f91621ef5d85), [OhWhenTheReds](https://polymarket.com/profile/0x918b42a06ff25eaaa4a79eca9da6a9de46f4ea63), [0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357](https://polymarket.com/profile/0x20d6436849f930584892730c7f96ebb2ac763856), [qwen300.fund](https://polymarket.com/profile/0xb0c85813a7a4428f1139ff91d3118a92c391fe7f), [aenews2](https://polymarket.com/profile/0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1), [ColdBlooded](https://polymarket.com/profile/0xbcc321b6336117432f4e9d2d28b20d8b6795ac9c), [rabbitfoot1](https://polymarket.com/profile/0x10a6fadcbacd66330862206f6199b197e3ad4d8b), [0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495](https://polymarket.com/profile/0xc7d02944a76b9f83b199e9090ecc92c82d241f8a), [pollo07](https://polymarket.com/profile/0x72487021e3339827c476592585c15ae7f0fa7e72), [zerone777](https://polymarket.com/profile/0xe949065b6c64308369c26dc590121623a5a4dea6), [TheReturnOfDarthMaul](https://polymarket.com/profile/0x3a8aa345d5db7ec5138298c8c4f4540259be7699), [scootergene](https://polymarket.com/profile/0xf3a6ac44c5c90ff2b4afa4459f71acc2e57971bd), [Eugycom](https://polymarket.com/profile/0x64ceab3becc143e1b97a8e16dc270c2297566015), [0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625](https://polymarket.com/profile/0x446884aa55e3dcf7123d9a3d6243c4e34b70b165), [Contestable-Parfait](https://polymarket.com/profile/0xc301c1e034e71e1a6ce9684f029c4674a00466aa), [pikachu2508](https://polymarket.com/profile/0x38891af2ad2f103ab8dc896c0243d2646deffe34), [lava-lava](https://polymarket.com/profile/0x629bc4a1e53e1d475beb7ea3d388791e96dd995a), [0xC9BFc7986767173b4f1c3FC9B2c6b255F](https://polymarket.com/profile/0xc9bfc7986767173b4f1c3fc9b2c6b255fc7381c0), [Likaseent](https://polymarket.com/profile/0x227f7ba7fcc35b7f8fc08aa6b075f5220da2a574), [Vale54holi](https://polymarket.com/profile/0x9d0dcd0c8aa0526303fd9e17fff4666ef52d2e6d), [GAMBLINGISCANCER69](https://polymarket.com/profile/0x9c56304c8840621ef4c1e707b4c7d708d09878d1), [dsasdaas](https://polymarket.com/profile/0x1e52bbdf389526f57abc62641d518868f4c5eb43), [wisewisewind](https://polymarket.com/profile/0xcdfb742c864b7011725b3b851291e326971497a0)

<details><summary>Leader trades we did <b>not</b> copy, and why</summary>

- leader trade too small / extreme price / crypto up-down: 150984
- per-market cap or out of cash: 17666
- market ends too soon: 7824
- signal too old (run was delayed): 219
- market already closed: 181
- price ran away from leader's price: 33
- order book too thin: 7

</details>

### Look-back test: if you had started copying 7 or 14 days ago

_Last calculated 28 Oct 2026 03:53 UTC. Copies each trade 20 min late, at a worse price (+0.01) and 1% fees._

| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |
|---|---:|---:|---:|---:|---:|
| 7 days ago | $1,000.00 | $1,202.03 | **+$202.03 (+20.2%)** | 220 | 78 / 85 |
| 14 days ago | $1,000.00 | $1,068.29 | **+$68.29 (+6.8%)** | 270 | 104 / 110 |

![backtest](data/backtest_wide_equity.svg)

| Trader | Bets | Profit/loss (14d) |
|---|---:|---:|
| lava-lava | 8 | +$147.41 |
| GAMBLINGISCANCER69 | 7 | +$115.38 |
| flawfence | 3 | +$85.87 |
| zerone777 | 4 | +$72.49 |
| RichieRicher | 14 | +$59.47 |
| 0xC9BFc7986767173b4f1c3FC9B2c6b255F | 40 | +$53.86 |
| Jsram | 7 | +$51.34 |
| Elaran1993 | 1 | +$19.40 |
| pollo07 | 2 | +$17.79 |
| ic4cream | 14 | +$13.90 |
| kaxel78 | 3 | +$13.54 |
| scootergene | 7 | +$6.49 |
| 0x20D6436849F930584892730C7F96eBB2Ac763856-1768642056357 | 8 | +$5.19 |
| Vale54holi | 2 | +$4.61 |
| 0xc7D02944A76B9F83B199e9090ECC92C82d241F8a-1776944395495 | 11 | -$0.15 |
| xtxpleasecallme | 1 | -$0.27 |
| Likaseent | 2 | -$1.12 |
| akroll | 3 | -$6.32 |
| ColdBlooded | 18 | -$11.30 |
| 123987456 | 2 | -$19.15 |
| mr.ozi | 9 | -$20.02 |
| primm | 1 | -$20.20 |
| para-Vision | 11 | -$21.22 |
| yabanci | 2 | -$21.23 |
| chongchong37 | 2 | -$22.26 |
| 0xA0b86991c6218b36c1d19D4a29Eb0cE3606eB4 | 19 | -$22.33 |
| VerilyWinningly | 8 | -$27.27 |
| paddaa | 14 | -$37.17 |
| rabbitfoot1 | 2 | -$40.40 |
| dsasdaas | 10 | -$42.81 |
| 0x448861155279dbf833d041b963e3ac854599e319 | 11 | -$48.17 |
| getbipped | 6 | -$67.25 |
| 0x446884aa55e3dCF7123D9A3D6243c4E34B70B165-1791060354625 | 13 | -$68.48 |
| dromedaryy | 5 | -$101.33 |

> ⚠️ **This look-back is flattering.** Traders are picked from *today's* leaderboard, partly *because* their recent bets won. The live paper test above is the honest number - judge the strategy on that.

<a id="top5"></a>
## Top 5 traders making $500k+/month

### Live paper trading (fake money, real prices)

| | |
|---|---|
| **Account value** | **$791.39** (started with $1,000.00) |
| **Profit / loss** | **-$208.61 (-20.9%)** |
| Running for | 7.4 days (since 20 Oct 2026 18:32 UTC) |
| Test period | until 2026-11-30 - then no new bets; open ones are held until they settle |
| Last update | 28 Oct 2026 03:50 UTC ✅ |
| Cash / in open bets | $0.00 / $791.39 |
| Bets opened | 47 (28 still open) |
| Finished bets won / lost | 7 / 12 (37% win rate) |

![live](data/live_top5_equity.svg)

#### Which traders are worth copying (live)

| Trader | Bets copied | Finished (won) | Profit/loss so far |
|---|---:|---:|---:|
| e46m3 | 35 | 12 (6) | -$57.27 |
| BreakTheBank | 12 | 7 (1) | -$151.34 |

**Currently copying 5 traders** (re-picked every 7 days, last on 27 Oct 2026 18:48 UTC): [BreakTheBank](https://polymarket.com/profile/0xf0318c32136c2db7fec88b84869aee6a1106c80c), [joseph00677](https://polymarket.com/profile/0xcdcccd0f2d86e450d973da415ad2430e5cc7935a), [e46m3](https://polymarket.com/profile/0x4f1d5ae26fc31472966e951af3183308736d8de2), [Bigggggggg](https://polymarket.com/profile/0x511f9c771449162349795d17becf8b37031acbe1), [takeormake](https://polymarket.com/profile/0xa38a455bbdd4b68486548b7e19da99903f4f821d)

<details><summary>Leader trades we did <b>not</b> copy, and why</summary>

- leader trade too small / extreme price / crypto up-down: 17033
- per-market cap or out of cash: 1393
- market ends too soon: 720
- signal too old (run was delayed): 28
- market already closed: 20
- price ran away from leader's price: 3

</details>

### Look-back test: if you had started copying 7 or 14 days ago

_Last calculated 28 Oct 2026 04:11 UTC. Copies each trade 20 min late, at a worse price (+0.01) and 1% fees._

| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |
|---|---:|---:|---:|---:|---:|
| 7 days ago | $1,000.00 | $1,173.28 | **+$173.28 (+17.3%)** | 79 | 17 / 15 |
| 14 days ago | $1,000.00 | $1,069.47 | **+$69.47 (+7.0%)** | 84 | 18 / 24 |

![backtest](data/backtest_top5_equity.svg)

| Trader | Bets | Profit/loss (14d) |
|---|---:|---:|
| juice-fruit | 10 | +$183.46 |
| e46m3 | 5 | +$92.84 |
| Bigggggggg | 42 | -$29.13 |
| joseph00677 | 8 | -$81.78 |
| BreakTheBank | 19 | -$95.93 |

> ⚠️ **This look-back is flattering.** Traders are picked from *today's* leaderboard, partly *because* their recent bets won. The live paper test above is the honest number - judge the strategy on that.

## Rules the bot follows

- Each strategy picks traders from the monthly leaderboard (All traders making $100k+/month (up to 60); Top 5 traders making $500k+/month) who are also profitable all-time, earn at least 3% on what they trade (filters out market-making bots) and made 3+ copyable trades in the last week. Re-picks weekly. Each strategy has its own separate fake account.
- When one of them buys ($100+, price between 0.05 and 0.95), the bot buys $20.00 of the same outcome at the real order-book price, max $60.00 per market.
- Skips it if the price has moved more than 0.03 past what the trader paid, if the market ends within 1h, or for 5/15-minute crypto 'Up or Down' markets (impossible to copy in time).
- Sells when the trader sells. Otherwise holds until the market resolves ($1 if right, $0 if wrong).
- Assumes 1% fees on every buy and sell (conservative).

Settings live in `config.json`. Raw data: `data/live_<strategy>_trades.csv`, `data/live_<strategy>_equity.csv`, `data/backtest_<strategy>.json`.

_Not financial advice. Past results, especially copied ones, don't guarantee future results._
