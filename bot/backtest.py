"""Replay the last 7 and 14 days: what would copying today's leaders have made?

Every leader buy is copied `backtest_delay_minutes` later at the market price then,
plus extra slippage and fees. Exits are copied the same way; markets that resolved
pay $1 / $0. Anything still open is valued at its latest price.
"""
import bisect
import time
from collections import Counter, defaultdict

from common import (CONFIG, profiles, Portfolio, copyable_buy, group_signals, market_info,
                    price_history, save_json, select_leaders, trades)


def price_at(hist, ts, max_gap=7200):
    """First recorded price at/after ts (what we could actually have traded at)."""
    if not hist:
        return None
    i = bisect.bisect_left(hist, (ts, -1.0))
    if i < len(hist) and hist[i][0] - ts <= max_gap:
        return hist[i][1]
    if i > 0 and ts - hist[i - 1][0] <= 3 * max_gap:  # quiet market: last known price
        return hist[i - 1][1]
    return None


def last_price_before(hist, ts):
    if not hist:
        return None
    i = bisect.bisect_right(hist, (ts, 2.0)) - 1
    return hist[i][1] if i >= 0 else None


def simulate(days, now, leaders, sigs, hists, meta, cfg):
    start = now - days * 86400
    delay = cfg["backtest_delay_minutes"] * 60
    slip = cfg["backtest_extra_slippage"]
    pf = Portfolio(None, cfg)
    skips = Counter()
    events = []  # (time, order, kind, payload)
    for s in sigs:
        if s["ts"] < start:
            continue
        t = s["ts"] + delay
        if t > now:
            continue
        if s["side"] == "BUY":
            events.append((t, 2, "buy", s))
        else:
            events.append((t, 1, "sell", s))
    settled = set()
    for tok, m in meta.items():
        if m.get("closed") and m.get("settle") is not None:
            ct = m.get("closed_ts") or m.get("end_ts")
            if not ct and hists.get(tok):
                ct = hists[tok][-1][0]
            if ct and ct <= now:
                events.append((ct, 0, "settle", tok))
    events.sort(key=lambda e: (e[0], e[1]))

    day_marks = [start + d * 86400 for d in range(days + 1)]
    curve, di = [], 0

    def snapshot(at):
        marks = {}
        for p in pf.positions.values():
            px = last_price_before(hists.get(p["token"]), at)
            if px is not None:
                marks[p["token"]] = px
        return pf.equity(marks)[0]

    for t, _, kind, x in events:
        while di < len(day_marks) and day_marks[di] <= t:
            curve.append([day_marks[di], round(snapshot(day_marks[di]), 2)])
            di += 1
        if kind == "settle":
            for k, p in list(pf.positions.items()):
                if p["token"] == x:
                    pf.close(k, meta[x]["settle"], t, "resolved")
            settled.add(x)
            continue
        s = x
        k = Portfolio.key(s["leader"], s["asset"])
        if kind == "sell":
            if k in pf.positions:
                px = price_at(hists.get(s["asset"]), t)
                if px is not None:
                    pf.close(k, max(0.0, px - slip), t, "leader sold")
            continue
        if not copyable_buy(s, cfg):
            skips["leader trade too small / extreme price / crypto up-down"] += 1
            continue
        if s["asset"] in settled:
            skips["market already closed"] += 1
            continue
        m = meta.get(s["asset"], {})
        if m.get("end_ts") and m["end_ts"] - t < cfg["min_hours_to_market_end"] * 3600:
            skips["market ends too soon"] += 1
            continue
        px = price_at(hists.get(s["asset"]), t)
        if px is None:
            skips["no price data"] += 1
            continue
        px = px + slip
        if px > s["price"] + cfg["max_slippage"] or px > 0.97:
            skips["price ran away from leader's price"] += 1
            continue
        room = cfg["max_per_market"] - pf.market_exposure(s["asset"])
        stake = min(cfg["stake_per_trade"], room, pf.cash / (1 + cfg["fee_rate"]))
        if stake < 1:
            skips["per-market cap or out of cash"] += 1
            continue
        pf.buy(s["leader"], s["leader_name"], s["asset"], px, stake / px, t, s["title"],
               s["outcome"], s["price"])
    while di < len(day_marks):
        curve.append([day_marks[di], round(snapshot(day_marks[di]), 2)])
        di += 1

    final_marks = {}
    for p in pf.positions.values():
        px = last_price_before(hists.get(p["token"]), now)
        if px is not None:
            final_marks[p["token"]] = px
    eq, pos_val = pf.equity(final_marks)
    curve[-1] = [now, round(eq, 2)]

    per = defaultdict(lambda: {"buys": 0, "closed": 0, "wins": 0, "realized": 0.0,
                               "unrealized": 0.0})
    for c in pf.closed:
        d = per[c["leader_name"]]
        d["closed"] += 1
        d["wins"] += c["pnl"] > 0
        d["realized"] += c["pnl"]
    for p in pf.positions.values():
        d = per[p["leader_name"]]
        mk = final_marks.get(p["token"], p["cost"] / p["shares"])
        d["unrealized"] += p["shares"] * mk - p["cost"]
    for p in list(pf.positions.values()) + pf.closed:
        per[p["leader_name"]]["buys"] += 1
    wins = sum(1 for c in pf.closed if c["pnl"] > 0)
    closed_sorted = sorted(pf.closed, key=lambda c: c["pnl"])
    bank = cfg["starting_bankroll"]
    return {
        "days": days,
        "start_ts": start,
        "end_ts": now,
        "starting_bankroll": bank,
        "final_equity": round(eq, 2),
        "pnl": round(eq - bank, 2),
        "return_pct": round((eq - bank) / bank * 100, 2),
        "cash": round(pf.cash, 2),
        "open_value": round(pos_val, 2),
        "positions_taken": len(pf.closed) + len(pf.positions),
        "closed_positions": len(pf.closed),
        "open_positions": len(pf.positions),
        "wins": wins,
        "losses": len(pf.closed) - wins,
        "realized_pnl": round(sum(c["pnl"] for c in pf.closed), 2),
        "per_leader": {k: {kk: round(vv, 2) if isinstance(vv, float) else vv
                           for kk, vv in v.items()} for k, v in per.items()},
        "skips": dict(skips),
        "curve": curve,
        "best": closed_sorted[-5:][::-1],
        "worst": closed_sorted[:5],
    }


def run(name, cfg):
    print(f"=== {name}: {cfg['label']}")
    now = int(time.time())
    if cfg.get("stop_new_bets_after"):
        from datetime import datetime
        if now > datetime.fromisoformat(cfg["stop_new_bets_after"]).timestamp():
            print("Test period is over; look-back test no longer updated.")
            return
    max_days = max(cfg["backtest_days"])
    start = now - max_days * 86400 - 3600
    print("Selecting leaders (today's leaderboard)...")
    leaders = select_leaders(cfg)
    sigs = []
    for l in leaders:
        rows = trades(l["wallet"], start=start, max_rows=5000)
        for s in group_signals(rows):
            s["leader"], s["leader_name"] = l["wallet"], l["name"]
            sigs.append(s)
        print(f"  {l['name']}: {len(rows)} fills")
    # only fetch prices for tokens we might actually trade
    buy_tokens = list(dict.fromkeys(s["asset"] for s in sigs if copyable_buy(s, cfg)))
    print(f"{len(sigs)} signals, {len(buy_tokens)} candidate markets")
    if len(buy_tokens) > 2500:
        buy_tokens = buy_tokens[-2500:]
    meta = market_info(buy_tokens)
    hists = {}
    for i, t in enumerate(buy_tokens):
        hists[t] = price_history(t, start - 3600, now, fidelity=5)
        if i % 100 == 0:
            print(f"  prices {i}/{len(buy_tokens)}")
        time.sleep(0.05)
    results = {str(d): simulate(d, now, leaders, sigs, hists, meta, cfg)
               for d in cfg["backtest_days"]}
    for d, r in results.items():
        print(f"{d} days: ${r['starting_bankroll']} -> ${r['final_equity']} ({r['return_pct']:+.1f}%),"
              f" {r['positions_taken']} positions")
    save_json(f"data/backtest_{name}.json", {"generated": now, "leaders": leaders, "config": cfg,
                                     "results": results})


def main():
    import os
    only = [x for x in os.environ.get("ONLY", "").split(",") if x]
    for name, cfg in profiles():
        if only and name not in only:
            continue
        try:
            run(name, cfg)
        except Exception:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
