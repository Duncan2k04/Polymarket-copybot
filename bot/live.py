"""One live paper-trading pass. Run every ~10 minutes by GitHub Actions.

Watches the selected leaders, copies their new buys/sells with fake money at the
real current order-book prices, settles resolved markets and records equity.
"""
import csv
import os
import time
from collections import Counter

from common import (CONFIG, Portfolio, book, copyable_buy, fill_buy, fill_sell, group_signals,
                    load_json, market_info, midpoint, path, save_json, select_leaders, trades)

STATE = "state/live.json"


def log_action(row):
    p = path("data", "live_trades.csv")
    new = not os.path.exists(p)
    with open(p, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["time_utc", "action", "leader", "market", "outcome",
                                          "leader_price", "our_price", "shares", "usd", "pnl",
                                          "note"])
        if new:
            w.writeheader()
        w.writerow(row)


def utc(ts):
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(ts))


def main():
    cfg = CONFIG
    now = int(time.time())
    st = load_json(STATE, {})
    st.setdefault("started", now)
    st.setdefault("last_seen", {})
    st.setdefault("skips", {})
    st.setdefault("runs", 0)
    pf = Portfolio(st.get("portfolio"), cfg)
    stop_ts = None
    if cfg.get("stop_new_bets_after"):
        from datetime import datetime
        stop_ts = int(datetime.fromisoformat(cfg["stop_new_bets_after"]).timestamp())
    finished = stop_ts is not None and now > stop_ts
    if finished:
        print("Test period is over: no new bets, only following exits and settling open ones.")
        if not pf.positions:
            print("All bets settled. Nothing left to do.")
            st["finished"] = True
            save_json(STATE, st)
            return

    # 1. (re)pick leaders weekly
    if not finished and not st.get("leaders") or not finished and now - st.get("leaders_refreshed", 0) > cfg["leader_refresh_days"] * 86400:
        print("Selecting leaders...")
        leaders = select_leaders(cfg)
        if leaders:
            history = st.setdefault("leader_history", [])
            history.append({"ts": now, "names": [l["name"] for l in leaders]})
            st["leaders"], st["leaders_refreshed"] = leaders, now
    leaders = {l["wallet"]: l["name"] for l in st.get("leaders", [])}
    # keep following anyone we still hold positions from, so we copy their exits too
    for p in pf.positions.values():
        leaders.setdefault(p["leader"], p["leader_name"])

    # 2. new signals
    skips = Counter()
    signals = []
    for w, name in leaders.items():
        since = st["last_seen"].get(w)
        if since is None:  # first time we see this leader: start from now, don't copy history
            st["last_seen"][w] = now
            continue
        rows = trades(w, start=since + 1, max_rows=2000)
        if rows:
            st["last_seen"][w] = max(int(r["timestamp"]) for r in rows)
        for s in group_signals(rows):
            s["leader"], s["leader_name"] = w, name
            signals.append(s)
        time.sleep(0.1)
    signals.sort(key=lambda s: s["ts"])
    print(f"{len(signals)} new signals from {len(leaders)} leaders")

    buy_tokens = [s["asset"] for s in signals if copyable_buy(s, cfg)]
    meta = market_info(buy_tokens) if buy_tokens else {}

    for s in signals:
        k = Portfolio.key(s["leader"], s["asset"])
        if s["side"] == "SELL":
            if k not in pf.positions:
                continue
            bids, _ = book(s["asset"])
            px = fill_sell(bids, pf.positions[k]["shares"]) if bids else midpoint(s["asset"])
            if px is None:
                skips["sell: no price"] += 1
                continue
            sh = pf.positions[k]["shares"]
            rec = pf.close(k, px, now, "leader sold")
            log_action({"time_utc": utc(now), "action": "SELL", "leader": s["leader_name"],
                        "market": s["title"][:90], "outcome": s["outcome"],
                        "leader_price": round(s["price"], 3), "our_price": round(px, 3),
                        "shares": round(sh, 2), "usd": round(rec["proceeds"], 2),
                        "pnl": round(rec["pnl"], 2), "note": "copied leader exit"})
            continue

        if finished:
            continue
        if not copyable_buy(s, cfg):
            skips["leader trade too small / extreme price / crypto up-down"] += 1
            continue
        if now - s["ts"] > cfg["max_signal_age_minutes"] * 60:
            skips["signal too old (run was delayed)"] += 1
            continue
        m = meta.get(s["asset"], {})
        if m.get("closed"):
            skips["market already closed"] += 1
            continue
        if m.get("end_ts") and m["end_ts"] - now < cfg["min_hours_to_market_end"] * 3600:
            skips["market ends too soon"] += 1
            continue
        room = cfg["max_per_market"] - pf.market_exposure(s["asset"])
        stake = min(cfg["stake_per_trade"], room, pf.cash / (1 + cfg["fee_rate"]))
        if stake < 1:
            skips["per-market cap or out of cash"] += 1
            continue
        _, asks = book(s["asset"])
        fill = fill_buy(asks, stake) if asks else None
        if not fill:
            skips["order book too thin"] += 1
            continue
        px, shares = fill
        if px > s["price"] + cfg["max_slippage"] or px > 0.97:
            skips["price ran away from leader's price"] += 1
            continue
        if pf.buy(s["leader"], s["leader_name"], s["asset"], px, shares, now, s["title"],
                  s["outcome"], s["price"]):
            log_action({"time_utc": utc(now), "action": "BUY", "leader": s["leader_name"],
                        "market": s["title"][:90], "outcome": s["outcome"],
                        "leader_price": round(s["price"], 3), "our_price": round(px, 3),
                        "shares": round(shares, 2), "usd": round(stake, 2), "pnl": "",
                        "note": f"leader spent ${s['usdc']:,.0f}"})

    # 3. settle resolved markets, mark the rest to market
    marks = {}
    open_tokens = list({p["token"] for p in pf.positions.values()})
    info = market_info(open_tokens) if open_tokens else {}
    for k, p in list(pf.positions.items()):
        i = info.get(p["token"], {})
        if i.get("closed") and i.get("settle") is not None:
            rec = pf.close(k, i["settle"], now, "resolved")
            log_action({"time_utc": utc(now), "action": "RESOLVED", "leader": p["leader_name"],
                        "market": p["title"][:90], "outcome": p["outcome"], "leader_price": "",
                        "our_price": i["settle"], "shares": round(p["shares"], 2),
                        "usd": round(rec["proceeds"], 2), "pnl": round(rec["pnl"], 2),
                        "note": "won" if i["settle"] >= 0.99 else ("lost" if i["settle"] <= 0.01 else "split")})
    for t in {p["token"] for p in pf.positions.values()}:
        m = midpoint(t)
        if m is not None:
            marks[t] = m
    eq, pos_val = pf.equity(marks)

    for reason, n in skips.items():
        st["skips"][reason] = st["skips"].get(reason, 0) + n
    st["runs"] += 1
    st["last_run"] = now
    st["marks"] = marks
    st["portfolio"] = pf.to_state()
    save_json(STATE, st)

    p = path("data", "live_equity.csv")
    new = not os.path.exists(p)
    with open(p, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts", "time_utc", "equity", "cash", "positions_value", "open_positions"])
        w.writerow([now, utc(now), round(eq, 2), round(pf.cash, 2), round(pos_val, 2),
                    len(pf.positions)])
    print(f"Equity ${eq:,.2f} (cash ${pf.cash:,.2f}, {len(pf.positions)} open positions)")


if __name__ == "__main__":
    main()
