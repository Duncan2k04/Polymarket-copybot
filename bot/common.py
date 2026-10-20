"""Shared helpers: Polymarket API access, leader selection, and the paper portfolio."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_API = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
UA = "Mozilla/5.0 (paper-copybot; read-only research)"


def path(*parts):
    return os.path.join(ROOT, *parts)


def load_json(rel, default):
    p = path(rel)
    if not os.path.exists(p):
        return default
    with open(p) as f:
        return json.load(f)


def save_json(rel, obj):
    p = path(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    os.replace(tmp, p)


CONFIG = load_json("config.json", {})


def profiles():
    """[(name, merged config)] - one paper account per profile, compared side by side."""
    out = []
    for name, over in (CONFIG.get("profiles") or {"main": {}}).items():
        cfg = {k: v for k, v in CONFIG.items() if k != "profiles"}
        cfg.update(over)
        cfg.setdefault("label", name)
        out.append((name, cfg))
    return out


# ---------------------------------------------------------------- HTTP

def http(method, url, params=None, body=None, retries=4):
    if params:
        url = url + "?" + urllib.parse.urlencode(params, doseq=True)
    data = json.dumps(body).encode() if body is not None else None
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode() or "null")
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (400, 404, 422):
                return None
            time.sleep(1.5 * (attempt + 1) ** 2)
        except Exception as e:  # network blips
            last = e
            time.sleep(1.5 * (attempt + 1) ** 2)
    print(f"  ! request failed {url[:140]}: {last}")
    return None


def get(url, params=None):
    return http("GET", url, params)


# ---------------------------------------------------------------- data API

def leaderboard(time_period="MONTH", order_by="PNL", limit=50, offset=0, user=None):
    params = {"timePeriod": time_period, "orderBy": order_by, "limit": limit,
              "offset": offset, "category": "OVERALL"}
    if user:
        params["user"] = user
    return get(f"{DATA_API}/v1/leaderboard", params) or []


def trades(user, start=None, end=None, max_rows=5000):
    """All TRADE activity for a wallet, newest first, optionally since `start` (epoch s)."""
    out, offset = [], 0
    while offset <= 5000 and len(out) < max_rows:
        params = {"user": user, "type": "TRADE", "limit": 500, "offset": offset,
                  "sortBy": "TIMESTAMP", "sortDirection": "DESC"}
        if start:
            params["start"] = int(start)
        if end:
            params["end"] = int(end)
        rows = get(f"{DATA_API}/activity", params)
        if not rows:
            break
        out.extend(rows)
        if len(rows) < 500:
            break
        offset += 500
        time.sleep(0.15)
    return out


# ---------------------------------------------------------------- markets

def _parse_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    try:
        return json.loads(v)
    except Exception:
        return []


def _parse_market(m):
    tokens = [str(t) for t in _parse_list(m.get("clobTokenIds"))]
    prices = _parse_list(m.get("outcomePrices"))
    outcomes = _parse_list(m.get("outcomes"))
    end = m.get("endDate") or m.get("endDateIso")
    end_ts = None
    if end:
        try:
            from datetime import datetime
            end_ts = int(datetime.fromisoformat(end.replace("Z", "+00:00")).timestamp())
        except Exception:
            end_ts = None
    closed_ts = None
    if m.get("closedTime"):
        try:
            from datetime import datetime
            ct = m["closedTime"].replace("Z", "+00:00").replace(" ", "T")
            if ct.endswith("+00"):
                ct += ":00"
            closed_ts = int(datetime.fromisoformat(ct).timestamp())
        except Exception:
            closed_ts = None
    res = {}
    for i, t in enumerate(tokens):
        settle = None
        if m.get("closed") and i < len(prices):
            try:
                p = float(prices[i])
                # only trust a clean resolution (1/0, or a 50-50 split)
                if p >= 0.99 or p <= 0.01 or abs(p - 0.5) < 1e-9:
                    settle = 1.0 if p >= 0.99 else (0.0 if p <= 0.01 else 0.5)
            except Exception:
                pass
        res[t] = {
            "question": m.get("question") or "",
            "slug": m.get("slug") or "",
            "outcome": outcomes[i] if i < len(outcomes) else "",
            "end_ts": end_ts,
            "closed": bool(m.get("closed")),
            "closed_ts": closed_ts,
            "settle": settle,
        }
    return res


def market_info(token_ids):
    """token_id -> market metadata (incl. settlement price if resolved)."""
    token_ids = [str(t) for t in dict.fromkeys(token_ids)]
    out = {}
    for i in range(0, len(token_ids), 25):
        chunk = token_ids[i:i + 25]
        rows = get(f"{GAMMA_API}/markets", {"clob_token_ids": chunk, "closed": "any",
                                            "limit": 100}) or []
        for m in rows:
            for t, info in _parse_market(m).items():
                if t in chunk:
                    out[t] = info
        time.sleep(0.1)
    # fall back to one-by-one for anything the batch call missed
    for t in token_ids:
        if t in out:
            continue
        for closed in ("any", "true", "false"):
            rows = get(f"{GAMMA_API}/markets", {"clob_token_ids": t, "closed": closed}) or []
            hit = False
            for m in rows:
                info = _parse_market(m)
                if t in info:
                    out[t] = info[t]
                    hit = True
            if hit:
                break
        time.sleep(0.05)
    return out


# ---------------------------------------------------------------- prices

def book(token_id):
    b = get(f"{CLOB_API}/book", {"token_id": token_id})
    if not b:
        return [], []
    bids = sorted(((float(x["price"]), float(x["size"])) for x in b.get("bids", [])),
                  key=lambda x: -x[0])
    asks = sorted(((float(x["price"]), float(x["size"])) for x in b.get("asks", [])),
                  key=lambda x: x[0])
    return bids, asks


def fill_buy(asks, dollars):
    """Walk the asks: returns (avg_price, shares) for spending `dollars`, or None if too thin."""
    spent = shares = 0.0
    for price, size in asks:
        take = min(size, (dollars - spent) / price)
        spent += take * price
        shares += take
        if spent >= dollars - 1e-6:
            return spent / shares, shares
    return None


def fill_sell(bids, shares):
    got = sold = 0.0
    for price, size in bids:
        take = min(size, shares - sold)
        got += take * price
        sold += take
        if sold >= shares - 1e-6:
            return got / sold
    return (got / sold) if sold > 0 else None


def midpoint(token_id):
    r = get(f"{CLOB_API}/midpoint", {"token_id": token_id})
    try:
        return float(r["mid"])
    except Exception:
        return None


def price_history(token_id, start_ts, end_ts, fidelity=5):
    r = get(f"{CLOB_API}/prices-history", {"market": token_id, "startTs": int(start_ts),
                                          "endTs": int(end_ts), "fidelity": fidelity})
    hist = (r or {}).get("history") or []
    if not hist:  # some markets reject long ranges at fine fidelity
        r = get(f"{CLOB_API}/prices-history", {"market": token_id, "interval": "max",
                                              "fidelity": 60})
        hist = (r or {}).get("history") or []
    return sorted((int(h["t"]), float(h["p"])) for h in hist)


# ---------------------------------------------------------------- signals

def group_signals(rows):
    """Collapse many partial fills into one signal per (asset, side, 10-min bucket)."""
    groups = {}
    for r in rows:
        if r.get("type") != "TRADE" or r.get("isCombo"):
            continue
        try:
            size, usdc, ts = float(r["size"]), float(r["usdcSize"]), int(r["timestamp"])
        except Exception:
            continue
        if size <= 0:
            continue
        key = (str(r["asset"]), r["side"], ts // 600)
        g = groups.setdefault(key, {"asset": str(r["asset"]), "side": r["side"], "size": 0.0,
                                    "usdc": 0.0, "ts": ts, "title": r.get("title", ""),
                                    "outcome": r.get("outcome", ""),
                                    "slug": r.get("eventSlug") or r.get("slug", "")})
        g["size"] += size
        g["usdc"] += usdc
        g["ts"] = max(g["ts"], ts)
    out = []
    for g in groups.values():
        g["price"] = g["usdc"] / g["size"]
        out.append(g)
    return sorted(out, key=lambda g: g["ts"])


def copyable_buy(sig, cfg=CONFIG):
    """Pre-filter on the leader's own trade (before looking at our price)."""
    if sig["side"] != "BUY":
        return False
    if sig["usdc"] < cfg["min_leader_trade_usdc"]:
        return False
    if not (cfg["min_price"] <= sig["price"] <= cfg["max_price"]):
        return False
    t = sig["title"].lower()
    if "up or down" in t:  # 5/15-minute crypto markets: impossible to copy with a delay
        return False
    return True


# ---------------------------------------------------------------- leader selection

def select_leaders(cfg=CONFIG, log=print):
    now = int(time.time())
    cands = []
    for off in range(0, 1000, 50):  # walk down the leaderboard until P/L drops below the bar
        page = leaderboard("MONTH", "PNL", 50, off)
        cands += page
        if len(page) < 50 or float(page[-1].get("pnl") or 0) < cfg["min_leader_month_pnl"]:
            break
    seen, picked = set(), []
    for c in cands:
        w = c.get("proxyWallet")
        if not w or w in seen:
            continue
        seen.add(w)
        pnl, vol = float(c.get("pnl") or 0), float(c.get("vol") or 0)
        name = c.get("userName") or w[:10]
        if pnl < cfg["min_leader_month_pnl"]:
            continue
        if vol <= 0 or pnl / vol < cfg["min_leader_pnl_to_volume"]:
            log(f"  skip {name}: thin margin ({pnl / max(vol, 1):.1%} of volume) - likely a market maker/bot")
            continue
        allt = leaderboard("ALL", "PNL", 1, 0, user=w)
        all_pnl = float(allt[0]["pnl"]) if allt else 0.0
        if all_pnl <= 0:
            log(f"  skip {name}: negative all-time P/L")
            continue
        recent = group_signals(trades(w, start=now - 7 * 86400, max_rows=1500))
        n_copy = sum(1 for s in recent if copyable_buy(s, cfg))
        if n_copy < cfg["min_copyable_trades_last_7d"]:
            log(f"  skip {name}: only {n_copy} copyable trades in last 7 days")
            continue
        picked.append({"wallet": w, "name": name, "month_pnl": round(pnl, 2),
                       "month_vol": round(vol, 2), "all_time_pnl": round(all_pnl, 2),
                       "copyable_7d": n_copy, "rank": c.get("rank")})
        log(f"  pick {name}: month P/L ${pnl:,.0f}, all-time ${all_pnl:,.0f}, {n_copy} copyable trades/7d")
        if len(picked) >= cfg["num_leaders"]:
            break
        time.sleep(0.1)
    return picked


# ---------------------------------------------------------------- portfolio

class Portfolio:
    """Paper portfolio. Positions are keyed by leader+token so results can be split per leader."""

    def __init__(self, state=None, cfg=CONFIG):
        state = state or {}
        self.cfg = cfg
        self.cash = state.get("cash", cfg["starting_bankroll"])
        self.positions = state.get("positions", {})
        self.closed = state.get("closed", [])

    def to_state(self):
        return {"cash": round(self.cash, 6), "positions": self.positions, "closed": self.closed}

    @staticmethod
    def key(leader, token):
        return f"{leader}|{token}"

    def market_exposure(self, token):
        return sum(p["cost"] for k, p in self.positions.items() if k.endswith("|" + token))

    def buy(self, leader, leader_name, token, price, shares, ts, title, outcome, leader_price):
        cost = price * shares
        fee = cost * self.cfg["fee_rate"]
        if cost + fee > self.cash + 1e-9:
            return False
        self.cash -= cost + fee
        k = self.key(leader, token)
        p = self.positions.get(k)
        if p:
            p["shares"] += shares
            p["cost"] += cost + fee
        else:
            self.positions[k] = {"leader": leader, "leader_name": leader_name, "token": token,
                                 "shares": shares, "cost": cost + fee, "opened": ts,
                                 "title": title, "outcome": outcome}
        self.positions[k].setdefault("buys", []).append(
            {"ts": ts, "price": round(price, 4), "leader_price": round(leader_price, 4),
             "shares": round(shares, 4)})
        return True

    def close(self, k, price, ts, reason):
        p = self.positions.pop(k)
        fee = 0.0 if reason == "resolved" else p["shares"] * price * self.cfg["fee_rate"]
        proceeds = p["shares"] * price - fee
        self.cash += proceeds
        rec = {"leader": p["leader"], "leader_name": p["leader_name"], "token": p["token"],
               "title": p["title"], "outcome": p["outcome"], "opened": p["opened"],
               "closed": ts, "cost": round(p["cost"], 4), "proceeds": round(proceeds, 4),
               "pnl": round(proceeds - p["cost"], 4), "exit_price": round(price, 4),
               "reason": reason}
        self.closed.append(rec)
        return rec

    def equity(self, marks):
        val = 0.0
        for p in self.positions.values():
            m = marks.get(p["token"])
            val += p["shares"] * (m if m is not None else p["cost"] / p["shares"])
        return self.cash + val, val
