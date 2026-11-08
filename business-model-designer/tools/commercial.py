#!/usr/bin/env python3
"""Commercial calculations for the business-model-designer.

Usage:
  python3 commercial.py contribution --price "49 USD" --fee "2.9% + 0.30 USD"|none|unknown --variable-cost "NAME=VALUE CUR"|none [...] [--json]
  python3 commercial.py timing --price "300 USD" --schedule upfront|split:50%,50%|monthly:N [--json]
  python3 commercial.py discount --list "49 USD" --discount "20%"|"10 USD" --bound "25%" [--floor "35 USD"] [--json]

Any money input may be "unknown". A calculation that needs an unknown input returns
"unknown" and names the missing input; it never substitutes a value. The fee and the
variable costs are stated, never defaulted: "none" declares that the transaction has none,
and an omitted variable cost leaves the contribution unknown.

Read-only and deterministic: no files written, no network, Decimal arithmetic rounded half-up
to the currency's cents. Expressions are written in the group's document form
("a − b = c"), so a result can be pasted into a document with its [derived: …] label.

Exit codes: 0 result (including an unknown result); 1 discount outside its bound or floor;
2 usage error (malformed amount, mixed currencies, schedule not summing to 100%).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")
UNKNOWN = "unknown"


class UsageError(Exception):
    pass


class Money:
    def __init__(self, amount: Decimal, currency: str):
        self.amount = amount
        self.currency = currency

    def __str__(self) -> str:
        return f"{self.amount.quantize(CENT, ROUND_HALF_UP)} {self.currency}"


def parse_money(text: str):
    """'49 USD', 'USD 49', '0.30 USD' -> Money; 'unknown' -> None."""
    t = text.strip()
    if t.lower() == UNKNOWN:
        return None
    m = re.fullmatch(r"([A-Z]{3})\s?(-?\d[\d,]*(?:\.\d+)?)|(-?\d[\d,]*(?:\.\d+)?)\s?([A-Z]{3})", t)
    if not m:
        raise UsageError(f"amount must carry a currency code, e.g. '49 USD': {text!r}")
    number = m.group(2) or m.group(3)
    currency = m.group(1) or m.group(4)
    try:
        return Money(Decimal(number.replace(",", "")), currency)
    except InvalidOperation as e:
        raise UsageError(f"malformed amount {text!r}") from e


def parse_percent(text: str):
    t = text.strip()
    if t.lower() == UNKNOWN:
        return None
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s?%", t)
    if not m:
        raise UsageError(f"percentage must read like '20%': {text!r}")
    return Decimal(m.group(1)) / 100


def parse_fee(text: str):
    """'2.9% + 0.30 USD', '2.9%', '0.30 USD', 'none', 'unknown' -> (rate, fixed Money|None) or None."""
    t = text.strip()
    if t.lower() == UNKNOWN:
        return None
    if t.lower() == "none":
        return Decimal(0), None
    rate, fixed = Decimal(0), None
    for part in [p.strip() for p in t.split("+")]:
        if part.endswith("%"):
            rate += parse_percent(part)
        else:
            fixed = parse_money(part)
            if fixed is None:
                return None
    return rate, fixed


def same_currency(*moneys):
    currencies = {m.currency for m in moneys if m is not None}
    if len(currencies) > 1:
        raise UsageError(f"mixed currencies {sorted(currencies)}; convert at a sourced rate before calculating")
    return currencies.pop() if currencies else None


def q(d: Decimal) -> Decimal:
    return d.quantize(CENT, ROUND_HALF_UP)


def fmt(d: Decimal, cur: str) -> str:
    return f"{q(d)} {cur}"


def pct(d: Decimal) -> str:
    return f"{(d * 100).normalize():f}%"


def contribution(price: str, fee: str, costs: list[str]) -> dict:
    p = parse_money(price)
    f = parse_fee(fee)
    named = []
    costs_stated = bool(costs)
    for c in costs:
        if c.strip().lower() == "none":
            continue
        if "=" not in c:
            raise UsageError(f"variable cost must read NAME=VALUE CUR: {c!r}")
        name, value = c.split("=", 1)
        named.append((name.strip(), parse_money(value)))
    fixed = f[1] if f else None
    cur = same_currency(p, fixed, *[m for _, m in named])
    missing = []
    if p is None:
        missing.append("price")
    if f is None:
        missing.append("fee")
    missing += [n for n, m in named if m is None]
    if not costs_stated:
        missing.append("variable costs (pass --variable-cost none when the transaction has none)")
    out = {"currency": cur, "missing": missing, "expressions": []}
    if p is None or f is None:
        out.update(fee=UNKNOWN, net_collected=UNKNOWN, contribution=UNKNOWN)
        return out
    rate, fixed = f
    fee_amount = q(p.amount * rate + (fixed.amount if fixed else 0))
    net = q(p.amount - fee_amount)
    if rate or fixed:
        parts = [f"{fmt(p.amount, cur)} × {pct(rate)}"] if rate else []
        if fixed:
            parts.append(fmt(fixed.amount, cur))
        if len(parts) > 1 or rate:
            out["expressions"].append(f"{' + '.join(parts)} = {fmt(fee_amount, cur)}")
    out["expressions"].append(f"{fmt(p.amount, cur)} − {fmt(fee_amount, cur)} = {fmt(net, cur)}")
    out.update(fee=fmt(fee_amount, cur), net_collected=fmt(net, cur))
    if not costs_stated or any(m is None for _, m in named):
        out["contribution"] = UNKNOWN
        return out
    total = net - sum((m.amount for _, m in named), Decimal(0))
    if named:
        terms = " − ".join([fmt(net, cur)] + [fmt(m.amount, cur) for _, m in named])
        out["expressions"].append(f"{terms} = {fmt(total, cur)}")
    out["contribution"] = fmt(total, cur)
    return out


def timing(price: str, schedule: str) -> dict:
    p = parse_money(price)
    if p is None:
        return {"schedule": schedule, "periods": UNKNOWN, "missing": ["price"]}
    if schedule == "upfront":
        shares = [Decimal(1)]
    elif schedule.startswith("split:"):
        shares = [parse_percent(s) for s in schedule[len("split:"):].split(",")]
        if any(s is None for s in shares) or sum(shares) != 1:
            raise UsageError("split shares must be known percentages summing to 100%")
    elif schedule.startswith("monthly:"):
        try:
            n = int(schedule[len("monthly:"):])
        except ValueError as e:
            raise UsageError("monthly schedule reads monthly:N") from e
        if n < 1:
            raise UsageError("monthly:N needs N >= 1")
        shares = [Decimal(1) / n] * n
    else:
        raise UsageError("schedule is upfront, split:A%,B%,… or monthly:N")
    amounts = [q(p.amount * s) for s in shares]
    amounts[-1] = q(p.amount - sum(amounts[:-1], Decimal(0)))  # remainder lands in the last period
    periods = [{"period": i, "amount": fmt(a, p.currency)} for i, a in enumerate(amounts)]
    expr = " + ".join(fmt(a, p.currency) for a in amounts) + f" = {fmt(sum(amounts, Decimal(0)), p.currency)}"
    return {"schedule": schedule, "periods": periods, "expression": expr, "missing": []}


def discount(list_price: str, disc: str, bound: str, floor: str | None) -> dict:
    lp = parse_money(list_price)
    b = parse_percent(bound)
    fl = parse_money(floor) if floor else None
    is_pct = disc.strip().endswith("%")
    d_pct = parse_percent(disc) if is_pct else None
    d_amt = None if is_pct else parse_money(disc)
    same_currency(lp, d_amt, fl)
    missing = [n for n, v in (("list price", lp), ("discount", d_pct if is_pct else d_amt), ("bound", b)) if v is None]
    if floor and fl is None:
        missing.append("floor")
    if lp is None or (d_pct is None and d_amt is None):
        return {"net_price": UNKNOWN, "within_authority": UNKNOWN, "missing": missing}
    cur = lp.currency
    if is_pct:
        cut = q(lp.amount * d_pct)
        rate = d_pct
        expr_cut = f"{fmt(lp.amount, cur)} × {pct(d_pct)} = {fmt(cut, cur)}"
    else:
        cut = q(d_amt.amount)
        rate = cut / lp.amount if lp.amount else Decimal(0)
        expr_cut = None
    net = q(lp.amount - cut)
    out = {"net_price": fmt(net, cur), "discount_rate": pct(rate.quantize(Decimal("0.0001"))),
           "expressions": [e for e in (expr_cut, f"{fmt(lp.amount, cur)} − {fmt(cut, cur)} = {fmt(net, cur)}") if e],
           "missing": missing}
    if b is None or (floor and fl is None):
        out["within_authority"] = UNKNOWN
        out["message"] = "bound unknown: the rule needs its approved bound before it can be applied"
        return out
    within = rate <= b and (fl is None or net >= fl.amount)
    out["within_authority"] = within
    if within:
        out["message"] = "within the approved bound"
    else:
        reasons = []
        if rate > b:
            reasons.append(f"discount {pct(rate.quantize(Decimal('0.0001')))} exceeds bound {pct(b)}")
        if fl is not None and net < fl.amount:
            reasons.append(f"net {fmt(net, cur)} is below floor {fmt(fl.amount, cur)}")
        out["message"] = "outside authority: " + "; ".join(reasons) + "; it needs a decision from the authority that set the bound"
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("contribution")
    c.add_argument("--price", required=True)
    c.add_argument("--fee", required=True)
    c.add_argument("--variable-cost", action="append", default=[])
    c.add_argument("--json", action="store_true")
    t = sub.add_parser("timing")
    t.add_argument("--price", required=True)
    t.add_argument("--schedule", required=True)
    t.add_argument("--json", action="store_true")
    d = sub.add_parser("discount")
    d.add_argument("--list", required=True)
    d.add_argument("--discount", required=True)
    d.add_argument("--bound", required=True)
    d.add_argument("--floor")
    d.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "contribution":
            out = contribution(args.price, args.fee, args.variable_cost)
        elif args.cmd == "timing":
            out = timing(args.price, args.schedule)
        else:
            out = discount(args.list, args.discount, args.bound, args.floor)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(out, indent=2, default=str))
    else:
        for k, v in out.items():
            if k == "expressions":
                for e in v:
                    print(f"expression: {e}")
            elif k == "periods" and isinstance(v, list):
                for p in v:
                    print(f"period {p['period']}: {p['amount']}")
            elif v not in ([], None):
                print(f"{k}: {', '.join(v) if isinstance(v, list) else v}")
    return 1 if args.cmd == "discount" and out.get("within_authority") is False else 0


if __name__ == "__main__":
    sys.exit(main())
