#!/usr/bin/env python3
"""Market-strategist supporting operations: transparent estimates, declared-scale scoring
with preference reversal, and qualification of a prospect against target-segments.

Usage:
  python3 market.py estimate FACTORS.csv [--json]
  python3 market.py score OPTIONS.csv --scale MIN-MAX --weights criterion=w,... [--json]
  python3 market.py qualify TARGET_SEGMENTS.md PROSPECT.json --target TGT-n [--json]

estimate  FACTORS.csv columns: factor,low,base,high,unit,basis. The estimate is the product
          of the factors at low, base and high. Units: a unit is "a", "a/b" or "%"; a
          denominator cancels an equal numerator of another factor; "%" and "share" are
          dimensionless (a % value is divided by 100). A factor whose value is "unknown" or
          empty, or whose basis is empty or "unknown", makes the estimate unknown: the
          result names each such factor and gives no number.
score     OPTIONS.csv columns: option, one column per criterion, optional basis. Every score
          lies on the declared scale (--scale). Reports weighted totals, the ranking, and the
          smallest change to one weight that makes another option overtake the top one.
qualify   Reads the Qualification table of a target-segments document. PROSPECT.json maps
          rule ids to the observed indicator: {"QR-1": true, "QR-2": false, "QR-3": null}.
          A missing id counts as null. A qualifier observed false, or a disqualifier observed
          true, disqualifies. Otherwise any null makes the result unknown, carrying each
          rule's "When unknown" treatment. Otherwise the prospect is qualified.

Read-only and deterministic. Exit 0 on a result (an unknown estimate or unknown
qualification is a result), 2 on invalid input.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".group" / "tools"))
import strategy_docs as sd  # noqa: E402

DIMENSIONLESS = {"", "%", "share", "ratio", "fraction"}


class InputError(Exception):
    pass


# ---- estimate ----------------------------------------------------------------
def parse_unit(unit: str) -> tuple[list[str], list[str]]:
    u = unit.strip()
    if u.lower() in DIMENSIONLESS:
        return [], []
    num, _, den = u.partition("/")
    return [t.strip() for t in num.split("*") if t.strip()], [t.strip() for t in den.split("*") if t.strip()]


def combine_units(units: list[str]) -> str:
    num: list[str] = []
    den: list[str] = []
    for u in units:
        n, d = parse_unit(u)
        num += n
        den += d
    for t in list(den):
        if t in num:
            num.remove(t)
            den.remove(t)
    if not num and not den:
        return "count"
    out = "*".join(num) or "1"
    return out + ("/" + "*".join(den) if den else "")


def read_number(value: str, unit: str) -> float | None:
    v = value.strip().replace(",", "")
    if v == "" or v.lower() == "unknown":
        return None
    try:
        x = float(v.rstrip("%"))
    except ValueError as e:
        raise InputError(f"not a number: {value!r}") from e
    return x / 100 if unit.strip() == "%" or v.endswith("%") else x


def estimate(rows: list[dict]) -> dict:
    required = {"factor", "low", "base", "high", "unit", "basis"}
    if not rows:
        raise InputError("no factors")
    if not required <= set(rows[0]):
        raise InputError(f"FACTORS.csv needs columns {sorted(required)}")
    missing, values, units = [], [], []
    for r in rows:
        basis = (r["basis"] or "").strip()
        nums = [read_number(r[k] or "", r["unit"] or "") for k in ("low", "base", "high")]
        if not basis or basis.lower() == "unknown" or any(n is None for n in nums):
            missing.append({"factor": r["factor"], "reason": "no basis" if not basis or basis.lower() == "unknown" else "value unknown"})
            continue
        low, base, high = nums
        if not low <= base <= high:
            raise InputError(f"factor {r['factor']!r}: low <= base <= high does not hold")
        values.append((low, base, high))
        units.append(r["unit"] or "")
    if missing:
        return {"estimate": "unknown", "missing": missing,
                "next": "obtain a basis for each missing factor, or leave the size unknown in the document"}
    low = base = high = 1.0
    for lo, b, hi in values:
        low, base, high = low * lo, base * b, high * hi
    return {"estimate": {"low": low, "base": base, "high": high}, "unit": combine_units(units),
            "factors": [r["factor"] for r in rows],
            "method": "product of factors; low and high multiply the factor bounds, so the range is the widest consistent with them"}


# ---- score -------------------------------------------------------------------
def parse_scale(s: str) -> tuple[float, float]:
    try:
        lo, hi = (float(x) for x in s.split("-", 1))
    except ValueError as e:
        raise InputError(f"--scale must be MIN-MAX, found {s!r}") from e
    if lo >= hi:
        raise InputError("--scale MIN must be below MAX")
    return lo, hi


def parse_weights(s: str) -> dict[str, float]:
    out = {}
    for part in s.split(","):
        k, _, v = part.partition("=")
        try:
            out[k.strip()] = float(v)
        except ValueError as e:
            raise InputError(f"weight {part!r} must be criterion=number") from e
        if out[k.strip()] < 0:
            raise InputError(f"weight {k!r} is negative")
    return out


def score(rows: list[dict], scale: tuple[float, float], weights: dict[str, float]) -> dict:
    if not rows or "option" not in rows[0]:
        raise InputError("OPTIONS.csv needs an 'option' column")
    criteria = [c for c in rows[0] if c not in ("option", "basis")]
    if set(weights) != set(criteria):
        raise InputError(f"weights must name exactly the criteria {criteria}")
    lo, hi = scale
    table = {}
    for r in rows:
        vals = {}
        for c in criteria:
            try:
                v = float(r[c])
            except (TypeError, ValueError) as e:
                raise InputError(f"{r['option']}: {c} is not on the declared scale: {r[c]!r}") from e
            if not lo <= v <= hi:
                raise InputError(f"{r['option']}: {c}={v} is outside the scale {lo}-{hi}")
            vals[c] = v
        table[r["option"]] = vals
    totals = {o: sum(weights[c] * v[c] for c in criteria) for o, v in table.items()}
    ranking = sorted(totals, key=lambda o: (-totals[o], o))
    top = ranking[0]
    reversal = None
    for other in ranking[1:]:
        diff = totals[top] - totals[other]
        for c in criteria:
            delta = table[top][c] - table[other][c]
            if delta == 0:
                continue
            d = -diff / delta  # weight change that equalises the two totals
            if weights[c] + d < 0:
                continue
            if reversal is None or abs(d) < abs(reversal["weight_change"]):
                reversal = {"criterion": c, "weight_change": round(d, 4), "from": weights[c],
                            "to": round(weights[c] + d, 4), "challenger": other}
    return {"totals": {o: round(totals[o], 4) for o in ranking}, "ranking": ranking, "top": top,
            "reversal": reversal or "no single-weight change reverses the top choice"}


# ---- qualify -----------------------------------------------------------------
def qualify(doc_path: Path, prospect: dict, target: str) -> dict:
    doc = sd.parse_document(doc_path, "target-segments")
    sec = doc.section("Qualification")
    table = next((t for t in sec.tables if t.col("ID") is not None and t.col("Kind") is not None), None) if sec else None
    if table is None:
        raise InputError("no Qualification table with ID and Kind columns")
    rules = []
    for row in table.rows:
        if target not in sd.ids_in(row[table.col("Target")]):
            continue
        rules.append({"id": sd.cell_text(row[table.col("ID")]), "kind": sd.cell_text(row[table.col("Kind")]).lower(),
                      "indicator": sd.cell_text(row[table.col("Indicator")]),
                      "when_unknown": sd.cell_text(row[table.col("When unknown")])})
    if not rules:
        raise InputError(f"no qualification rule applies to {target}")
    failed, unknown = [], []
    for r in rules:
        observed = prospect.get(r["id"])
        if observed not in (True, False, None):
            raise InputError(f"{r['id']} must be true, false or null")
        if observed is None:
            unknown.append(r)
        elif (r["kind"] == "qualifier" and observed is False) or (r["kind"] == "disqualifier" and observed is True):
            failed.append(r)
    if failed:
        result = "disqualified"
    elif unknown:
        result = "unknown"
    else:
        result = "qualified"
    return {"target": target, "result": result,
            "failed": [{"id": r["id"], "indicator": r["indicator"]} for r in failed],
            "unknown": [{"id": r["id"], "indicator": r["indicator"], "treatment": r["when_unknown"]} for r in unknown]}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("estimate"); e.add_argument("factors", type=Path); e.add_argument("--json", action="store_true")
    s = sub.add_parser("score"); s.add_argument("options", type=Path); s.add_argument("--scale", required=True)
    s.add_argument("--weights", required=True); s.add_argument("--json", action="store_true")
    q = sub.add_parser("qualify"); q.add_argument("doc", type=Path); q.add_argument("prospect", type=Path)
    q.add_argument("--target", required=True); q.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "estimate":
            out = estimate(read_csv(args.factors))
        elif args.cmd == "score":
            out = score(read_csv(args.options), parse_scale(args.scale), parse_weights(args.weights))
        else:
            out = qualify(args.doc, json.loads(args.prospect.read_text(encoding="utf-8")), args.target)
    except (InputError, OSError, json.JSONDecodeError, StopIteration) as err:
        print(f"invalid input: {err}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2, ensure_ascii=False) if args.json else render(args.cmd, out))
    return 0


def render(cmd: str, out: dict) -> str:
    if cmd == "estimate":
        if out["estimate"] == "unknown":
            return "estimate: unknown\n" + "\n".join(f"  missing {m['factor']}: {m['reason']}" for m in out["missing"]) + f"\nnext: {out['next']}"
        e = out["estimate"]
        return f"estimate: {e['low']:g} – {e['high']:g} {out['unit']} (base {e['base']:g})\nmethod: {out['method']}"
    if cmd == "score":
        lines = [f"{i + 1}. {o}: {t}" for i, (o, t) in enumerate(out["totals"].items())]
        rv = out["reversal"]
        lines.append(f"reversal: {rv}" if isinstance(rv, str) else
                     f"reversal: {rv['challenger']} overtakes {out['top']} when weight of {rv['criterion']} moves {rv['from']} → {rv['to']}")
        return "\n".join(lines)
    lines = [f"{out['target']}: {out['result']}"]
    lines += [f"  fails {r['id']}: {r['indicator']}" for r in out["failed"]]
    lines += [f"  unknown {r['id']}: {r['indicator']} → {r['treatment']}" for r in out["unknown"]]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
