"""Rebuild README.md (the dashboard you read on GitHub) from the saved data."""
import csv
import os
import time
from collections import defaultdict

from common import CONFIG, load_json, path

GREEN, RED, GREY = "#1a7f37", "#cf222e", "#8c959f"


def money(x, sign=False):
    s = f"${abs(x):,.2f}"
    if sign:
        return ("+" if x >= 0 else "-") + s
    return ("-" if x < 0 else "") + s


def day(ts):
    return time.strftime("%d %b %Y %H:%M UTC", time.gmtime(ts))


def svg_chart(points, base, fname, title):
    """Tiny dependency-free line chart. points = [(ts, value)]."""
    W, H, P = 720, 260, 48
    if len(points) < 2:
        points = (points or [(time.time(), base)]) * 2
    xs = [p[0] for p in points]
    ys = [p[1] for p in points] + [base]
    x0, x1 = min(xs), max(xs) or 1
    y0, y1 = min(ys), max(ys)
    pad = max((y1 - y0) * 0.1, base * 0.01)
    y0, y1 = y0 - pad, y1 + pad
    sx = lambda x: P + (x - x0) / max(x1 - x0, 1) * (W - 2 * P)
    sy = lambda y: H - P + 10 - (y - y0) / (y1 - y0) * (H - 2 * P)
    col = GREEN if points[-1][1] >= base else RED
    line = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in points)
    by = sy(base)
    labels = ""
    for v in (y0 + pad, base, y1 - pad):
        labels += (f'<text x="{P - 6}" y="{sy(v) + 4:.1f}" font-size="11" text-anchor="end" '
                   f'fill="#57606a">${v:,.0f}</text>')
    labels += (f'<text x="{P}" y="{H - 8}" font-size="11" fill="#57606a">'
               f'{time.strftime("%d %b", time.gmtime(x0))}</text>'
               f'<text x="{W - P}" y="{H - 8}" font-size="11" text-anchor="end" fill="#57606a">'
               f'{time.strftime("%d %b", time.gmtime(x1))}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'font-family="Helvetica,Arial,sans-serif"><rect width="{W}" height="{H}" fill="#ffffff"/>'
           f'<text x="{P}" y="22" font-size="14" font-weight="bold" fill="#24292f">{title}</text>'
           f'<line x1="{P}" x2="{W - P}" y1="{by:.1f}" y2="{by:.1f}" stroke="{GREY}" '
           f'stroke-dasharray="4 4"/>{labels}'
           f'<polyline points="{line}" fill="none" stroke="{col}" stroke-width="2.5"/></svg>')
    with open(path("data", fname), "w") as f:
        f.write(svg)
    return f"data/{fname}"


def read_csv(name):
    p = path("data", name)
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return list(csv.DictReader(f))


def live_section(cfg):
    st = load_json("state/live.json", None)
    if not st:
        return ["## Live paper trading", "", "_Not started yet. First run is due shortly._", ""]
    bank = cfg["starting_bankroll"]
    eq_rows = read_csv("live_equity.csv")
    pts = [(int(r["ts"]), float(r["equity"])) for r in eq_rows]
    step = max(1, len(pts) // 400)
    pts_d = pts[::step] + ([pts[-1]] if pts and pts[-1] not in pts[::step] else [])
    eq = pts[-1][1] if pts else bank
    pnl = eq - bank
    pf = st.get("portfolio", {})
    closed = pf.get("closed", [])
    wins = sum(1 for c in closed if c["pnl"] > 0)
    days = (st.get("last_run", st["started"]) - st["started"]) / 86400
    stale = time.time() - st.get("last_run", 0) > 3 * 3600
    chart = svg_chart(pts_d, bank, "live_equity.svg", "Live paper account value")
    out = [
        "## Live paper trading (fake money, real prices)",
        "",
        f"| | |", "|---|---|",
        f"| **Account value** | **{money(eq)}** (started with {money(bank)}) |",
        f"| **Profit / loss** | **{money(pnl, True)} ({pnl / bank * 100:+.1f}%)** |",
        f"| Running for | {days:.1f} days (since {day(st['started'])}) |",
        f"| Last update | {day(st.get('last_run', 0))}"
        + (" ⚠️ **no update for 3+ hours - check the Actions tab**" if stale else " ✅") + " |",
        f"| Cash / in open bets | {money(pf.get('cash', bank))} / {money(eq - pf.get('cash', bank))} |",
        f"| Bets opened | {len(closed) + len(pf.get('positions', {}))} "
        f"({len(pf.get('positions', {}))} still open) |",
        f"| Finished bets won / lost | {wins} / {len(closed) - wins}"
        + (f" ({wins / len(closed) * 100:.0f}% win rate)" if closed else "") + " |",
        "",
        f"![live]({chart})",
        "",
    ]
    # per leader
    per = defaultdict(lambda: {"n": 0, "real": 0.0, "unreal": 0.0, "w": 0, "c": 0})
    marks = st.get("marks", {})
    for c in closed:
        d = per[c["leader_name"]]
        d["n"] += 1; d["c"] += 1; d["real"] += c["pnl"]; d["w"] += c["pnl"] > 0
    for p in pf.get("positions", {}).values():
        d = per[p["leader_name"]]
        d["n"] += 1
        mk = marks.get(p["token"], p["cost"] / p["shares"])
        d["unreal"] += p["shares"] * mk - p["cost"]
    if per:
        out += ["### Which traders are worth copying (live)", "",
                "| Trader | Bets copied | Finished (won) | Profit/loss so far |",
                "|---|---:|---:|---:|"]
        for name, d in sorted(per.items(), key=lambda kv: -(kv[1]["real"] + kv[1]["unreal"])):
            out.append(f"| {name} | {d['n']} | {d['c']} ({d['w']}) | "
                       f"{money(d['real'] + d['unreal'], True)} |")
        out.append("")
    leaders = st.get("leaders", [])
    if leaders:
        out += [f"**Currently copying {len(leaders)} traders** (re-picked every "
                f"{cfg['leader_refresh_days']} days, last on {day(st.get('leaders_refreshed', 0))}): "
                + ", ".join(f"[{l['name']}](https://polymarket.com/profile/{l['wallet']})"
                            for l in leaders), ""]
    acts = read_csv("live_trades.csv")[-20:][::-1]
    if acts:
        out += ["### Latest activity", "", "| Time (UTC) | Action | Trader | Market | Side | Price | $ | P/L |",
                "|---|---|---|---|---|---:|---:|---:|"]
        for a in acts:
            out.append(f"| {a['time_utc']} | {a['action']} | {a['leader']} | {a['market'][:60]} | "
                       f"{a['outcome']} | {a['our_price']} | {a['usd']} | {a['pnl']} |")
        out.append("")
    if st.get("skips"):
        out += ["<details><summary>Leader trades we did <b>not</b> copy, and why</summary>", ""]
        for k, v in sorted(st["skips"].items(), key=lambda kv: -kv[1]):
            out.append(f"- {k}: {v}")
        out += ["", "</details>", ""]
    return out


def backtest_section(cfg):
    bt = load_json("data/backtest.json", None)
    if not bt:
        return ["## Look-back test", "", "_Running... results will appear here._", ""]
    out = ["## Look-back test: if you had started copying 7 or 14 days ago", "",
           f"_Last calculated {day(bt['generated'])}. Copies each trade "
           f"{cfg['backtest_delay_minutes']} min late, at a worse price "
           f"(+{cfg['backtest_extra_slippage']:.2f}) and {cfg['fee_rate']:.0%} fees._", "",
           "| Started | Deposit | Value now | Profit/loss | Bets | Finished won / lost |",
           "|---|---:|---:|---:|---:|---:|"]
    for d, r in sorted(bt["results"].items(), key=lambda kv: int(kv[0])):
        out.append(f"| {d} days ago | {money(r['starting_bankroll'])} | {money(r['final_equity'])} | "
                   f"**{money(r['pnl'], True)} ({r['return_pct']:+.1f}%)** | {r['positions_taken']} | "
                   f"{r['wins']} / {r['losses']} |")
    out.append("")
    longest = bt["results"][str(max(int(k) for k in bt["results"]))]
    chart = svg_chart([tuple(p) for p in longest["curve"]], longest["starting_bankroll"],
                      "backtest_equity.svg", f"Look-back: last {longest['days']} days")
    out += [f"![backtest]({chart})", "", "| Trader | Bets | Profit/loss (14d) |", "|---|---:|---:|"]
    for name, d in sorted(longest["per_leader"].items(),
                          key=lambda kv: -(kv[1]["realized"] + kv[1]["unrealized"])):
        out.append(f"| {name} | {d['buys']} | {money(d['realized'] + d['unrealized'], True)} |")
    out += ["", "> ⚠️ **This look-back is flattering.** Traders are picked from *today's* "
            "leaderboard, partly *because* their recent bets won. The live paper test above is "
            "the honest number - judge the strategy on that.", ""]
    return out


def main():
    cfg = CONFIG
    lines = ["# Polymarket copy-trading bot (paper money)", "",
             "Copies the trades of top Polymarket traders using a **fake "
             f"{money(cfg['starting_bankroll'])} account** and real market prices. "
             "No real money, no wallet, no keys. Runs by itself every ~10 minutes on GitHub Actions.",
             ""]
    lines += live_section(cfg)
    lines += backtest_section(cfg)
    lines += [
        "## Rules the bot follows", "",
        f"- Picks the top {cfg['num_leaders']} traders on the monthly leaderboard who: made "
        f"${cfg['min_leader_month_pnl']:,}+ this month, are profitable all-time, earn at least "
        f"{cfg['min_leader_pnl_to_volume']:.0%} on what they trade (filters out market-making bots) "
        f"and made {cfg['min_copyable_trades_last_7d']}+ copyable trades in the last week. Re-picks weekly.",
        f"- When one of them buys (${cfg['min_leader_trade_usdc']}+, price between "
        f"{cfg['min_price']:.2f} and {cfg['max_price']:.2f}), the bot buys "
        f"{money(cfg['stake_per_trade'])} of the same outcome at the real order-book price, "
        f"max {money(cfg['max_per_market'])} per market.",
        f"- Skips it if the price has moved more than {cfg['max_slippage']:.2f} past what the "
        f"trader paid, if the market ends within {cfg['min_hours_to_market_end']}h, or for "
        "5/15-minute crypto 'Up or Down' markets (impossible to copy in time).",
        "- Sells when the trader sells. Otherwise holds until the market resolves ($1 if right, $0 if wrong).",
        f"- Assumes {cfg['fee_rate']:.0%} fees on every buy and sell (conservative).",
        "",
        "Settings live in `config.json`. Raw data: `data/live_trades.csv`, `data/live_equity.csv`, "
        "`data/backtest.json`.",
        "",
        "_Not financial advice. Past results, especially copied ones, don't guarantee future results._",
    ]
    with open(path("README.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
