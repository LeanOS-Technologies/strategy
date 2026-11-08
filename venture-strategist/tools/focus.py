#!/usr/bin/env python3
"""Focus-plan support for venture-strategist: the ready set and outcome comparison.

Usage:
  python3 focus.py ready FOCUS_PLAN.md [--satisfied ID-or-condition ...] [--json]
  python3 focus.py compare --expected "VALUE UNIT" --observed "VALUE UNIT" [--json]

ready
  Reads the focus-plan's Work sequence (ID, Timing, Prerequisite) and Enabling actions (ID).
  A Prerequisite cell is `none`, or ACT/ENB ids, or a named condition, or ids plus a condition.
  An id prerequisite means the output of that action or enabling step exists; it is satisfied
  only when named in --satisfied. A named condition is satisfied when --satisfied names it
  (case- and whitespace-insensitive). Enabling actions carry no prerequisite and are ready.

  Ready(A) = actions whose prerequisites are all satisfied.

  Findings (level, code):
    error   CYCLE           actions whose id prerequisites form a cycle
    error   UNDECLARED      a prerequisite id that no row declares
    error   TIMING-UNREADY  an action timed now or parallel whose prerequisites are not satisfied
    info    WAITING-READY   an action timed after whose prerequisites are satisfied
    info    DEFERRED-READY  an action timed deferred that is ready (intentional deferral is allowed)

compare
  Difference (observed - expected) and ratio (observed / expected) of two values in the same
  unit. `unknown` on either side is not comparable: exit 3, nothing computed.

Read-only and deterministic. Exit codes: 0 no error findings / compared; 1 error findings;
2 unreadable input or incompatible units; 3 a value is unknown.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".group" / "tools"))
import strategy_docs as sd  # noqa: E402


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def parse_prerequisite(cell: str) -> tuple[list[str], list[str]]:
    """Return (ids, named conditions) of a Prerequisite cell."""
    text = sd.cell_text(cell)
    if not text or text.lower() in ("none", "n/a", "-", "—"):
        return [], []
    ids = sd.ids_in(text)
    rest = sd.ID_RE.sub("", text)
    rest = re.sub(r"\b(and|or)\b", " ", rest, flags=re.I)
    rest = rest.strip(" ,;+&")
    conditions = [norm(c) for c in re.split(r"[;,]", rest) if norm(c).strip(" .")]
    return ids, conditions


def load_plan(path: Path):
    doc = sd.parse_document(path, "focus-plan")
    ws = doc.section("Work sequence")
    if ws is None:
        raise ValueError("focus-plan has no 'Work sequence' section")
    table = next((t for t in ws.tables if t.col("ID") is not None and t.col("Prerequisite") is not None), None)
    if table is None:
        raise ValueError("'Work sequence' needs a table with ID, Timing and Prerequisite columns")
    actions = []
    for row in table.rows:
        ids, conds = parse_prerequisite(row[table.col("Prerequisite")])
        actions.append({
            "id": sd.cell_text(row[table.col("ID")]),
            "timing": sd.cell_text(row[table.col("Timing")]).lower() if table.col("Timing") is not None else "",
            "prereq_ids": ids,
            "prereq_conditions": conds,
        })
    enabling = []
    en = doc.section("Enabling actions")
    if en is not None:
        t = next((t for t in en.tables if t.col("ID") is not None), None)
        if t is not None:
            enabling = [sd.cell_text(r[t.col("ID")]) for r in t.rows]
    return actions, enabling


def find_cycles(actions) -> list[list[str]]:
    graph = {a["id"]: [p for p in a["prereq_ids"] if p.startswith("ACT-")] for a in actions}
    cycles, state, stack = [], {}, []

    def visit(n):
        state[n] = 1
        stack.append(n)
        for m in graph.get(n, []):
            if state.get(m) == 1:
                cycle = stack[stack.index(m):]
                if sorted(cycle) not in [sorted(c) for c in cycles]:
                    cycles.append(list(cycle))
            elif state.get(m) is None and m in graph:
                visit(m)
        stack.pop()
        state[n] = 2

    for n in sorted(graph):
        if state.get(n) is None:
            visit(n)
    return cycles


def ready(actions, enabling, satisfied: list[str]) -> dict:
    sat_ids = {s.strip() for s in satisfied if sd.ID_RE.fullmatch(s.strip())}
    sat_conds = {norm(s) for s in satisfied if not sd.ID_RE.fullmatch(s.strip())}
    declared = {a["id"] for a in actions} | set(enabling)
    findings = []
    ready_ids = []
    for a in actions:
        for p in a["prereq_ids"]:
            if p not in declared:
                findings.append({"level": "error", "code": "UNDECLARED", "action": a["id"], "message": f"prerequisite {p} is not declared in the plan"})
        unmet = [p for p in a["prereq_ids"] if p not in sat_ids] + [c for c in a["prereq_conditions"] if c not in sat_conds]
        a_ready = not unmet
        if a_ready:
            ready_ids.append(a["id"])
        if a["timing"] in ("now", "parallel") and not a_ready:
            findings.append({"level": "error", "code": "TIMING-UNREADY", "action": a["id"], "message": f"timed {a['timing']} but waits on {unmet}"})
        elif a["timing"] == "after" and a_ready:
            findings.append({"level": "info", "code": "WAITING-READY", "action": a["id"], "message": "timed after but every prerequisite is satisfied"})
        elif a["timing"] == "deferred" and a_ready:
            findings.append({"level": "info", "code": "DEFERRED-READY", "action": a["id"], "message": "ready; deferred by choice"})
    for cycle in find_cycles(actions):
        findings.append({"level": "error", "code": "CYCLE", "action": cycle[0], "message": "dependency cycle " + " -> ".join(cycle + [cycle[0]])})
    return {"ready": ready_ids + list(enabling), "findings": findings}


VALUE_RE = re.compile(r"^\s*([-+]?\d[\d,]*(?:\.\d+)?)\s*(%|[A-Za-z][A-Za-z -]*)?\s*$")


def parse_value(s: str):
    if s.strip().lower().startswith("unknown"):
        return None
    m = VALUE_RE.match(s)
    if not m:
        raise ValueError(f"cannot read value {s!r}; write 'VALUE UNIT'")
    unit = (m.group(2) or "").strip()
    unit = unit if unit.isupper() or unit == "%" else unit.lower().rstrip("s")
    return float(m.group(1).replace(",", "")), unit


def compare(expected: str, observed: str) -> dict:
    e, o = parse_value(expected), parse_value(observed)
    if e is None or o is None:
        return {"comparable": False, "reason": "a value is unknown; record the observation needed"}
    if e[1] != o[1]:
        raise ValueError(f"incompatible units: {e[1] or 'none'} and {o[1] or 'none'}")
    return {
        "comparable": True,
        "unit": e[1],
        "expected": e[0],
        "observed": o[0],
        "difference": round(o[0] - e[0], 10),
        "ratio": None if e[0] == 0 else round(o[0] / e[0], 6),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("ready")
    r.add_argument("plan", type=Path)
    r.add_argument("--satisfied", nargs="*", default=[])
    r.add_argument("--json", action="store_true")
    c = sub.add_parser("compare")
    c.add_argument("--expected", required=True)
    c.add_argument("--observed", required=True)
    c.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "ready":
        try:
            actions, enabling = load_plan(args.plan)
        except (OSError, ValueError, IndexError) as e:
            print(f"unreadable focus-plan: {e}", file=sys.stderr)
            return 2
        result = ready(actions, enabling, args.satisfied)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Ready(A): " + (", ".join(result["ready"]) or "none"))
            for f in result["findings"]:
                print(f"{f['level']:6} {f['code']:15} {f['action']}  {f['message']}")
        return 1 if any(f["level"] == "error" for f in result["findings"]) else 0

    try:
        result = compare(args.expected, args.observed)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    elif not result["comparable"]:
        print(result["reason"])
    else:
        print(f"difference {result['difference']} {result['unit']}; ratio {result['ratio']}")
    return 0 if result["comparable"] else 3


if __name__ == "__main__":
    sys.exit(main())
