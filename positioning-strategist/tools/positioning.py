#!/usr/bin/env python3
"""Check advantage chains in a differentiation document, and their use in positioning and offers.

Usage:
  python3 positioning.py check DIFFERENTIATION.md [--positioning POSITIONING_DECISION.md]
                                                  [--offers OFFER_CATALOGUE.md] [--json]

Findings:
  error   AGAINST      an advantage's Against names no declared ALT id, or an undeclared one
  error   SUPPORT      an advantage has no Support and trade-offs row
  error   DEVELOPMENT  a planned or unknown capability has no proof or development need (empty or 'none')
  info    UNUSED-ALT   an alternative no advantage is compared against
  review  PLANNED-FRAME   the positioning decision cites an advantage whose capability is planned or unknown
  review  PLANNED-OFFER   an available offer cites an advantage whose capability is planned or unknown

The tool checks references and availability status; it does not judge whether a frame or
offer presents the capability accurately. Review findings go to specialist evaluation.

Read-only and deterministic. Exit 0 with no errors, 1 with errors, 2 when a document cannot be read.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".group" / "tools"))
import strategy_docs as sd  # noqa: E402


def table(doc: sd.Document, section: str, column: str):
    sec = doc.section(section)
    if sec is None:
        return None
    return next((t for t in sec.tables if t.col(column) is not None), None)


def check(diff_path: Path, positioning: Path | None = None, offers: Path | None = None) -> list[dict]:
    findings: list[dict] = []

    def add(level, rule, path, line, msg):
        findings.append({"level": level, "rule": rule, "path": str(path), "line": line, "message": msg})

    doc = sd.parse_document(diff_path, "differentiation")
    alt_t = table(doc, "Alternative basis", "ID")
    adv_t = table(doc, "Advantage chains", "Availability")
    sup_t = table(doc, "Support and trade-offs", "Advantage")
    alts = {sd.cell_text(r[alt_t.col("ID")]): alt_t.line + 2 + i for i, r in enumerate(alt_t.rows)} if alt_t else {}
    availability: dict[str, str] = {}
    used_alts: set[str] = set()
    if adv_t is None:
        add("error", "AGAINST", diff_path, 1, "no 'Advantage chains' table with an Availability column")
        return findings
    for i, r in enumerate(adv_t.rows):
        line = adv_t.line + 2 + i
        adv = sd.cell_text(r[adv_t.col("ID")])
        availability[adv] = sd.cell_text(r[adv_t.col("Availability")]).lower()
        against = [x for x in sd.ids_in(r[adv_t.col("Against")]) if x.startswith("ALT-")]
        if not against:
            add("error", "AGAINST", diff_path, line, f"{adv} is compared against no declared alternative; name the ALT ids")
        for a in against:
            if a not in alts:
                add("error", "AGAINST", diff_path, line, f"{adv} is compared against {a}, which Alternative basis does not declare")
            used_alts.add(a)
    support: dict[str, tuple[int, str]] = {}
    if sup_t is not None:
        need_col = sup_t.col("Needed proof or development")
        for i, r in enumerate(sup_t.rows):
            for adv in sd.ids_in(r[sup_t.col("Advantage")]):
                need = sd.cell_text(r[need_col]) if need_col is not None and need_col < len(r) else ""
                support[adv] = (sup_t.line + 2 + i, need)
    for adv, avail in availability.items():
        if adv not in support:
            add("error", "SUPPORT", diff_path, adv_t.line, f"{adv} has no Support and trade-offs row")
            continue
        line, need = support[adv]
        if avail in ("planned", "unknown") and need.lower() in ("", "none", "n/a"):
            add("error", "DEVELOPMENT", diff_path, line, f"{adv} is {avail}; name the proof or development it needs")
    for a, line in alts.items():
        if a not in used_alts:
            add("info", "UNUSED-ALT", diff_path, line, f"{a} is declared but no advantage is compared against it")

    not_current = {a for a, v in availability.items() if v in ("planned", "unknown")}

    if positioning is not None:
        pdoc = sd.parse_document(positioning, "positioning-decision")
        for sec_name in ("Conclusion", "Positioning choice", "Frame meaning"):
            sec = pdoc.section(sec_name)
            if sec is None:
                continue
            for off, raw in enumerate(sec.text.splitlines()):
                for adv in sorted(set(re.findall(r"\bADV-\d+\b", raw)) & not_current):
                    add("review", "PLANNED-FRAME", positioning, sec.line + 1 + off,
                        f"{sec_name} cites {adv}, whose capability is {availability[adv]}; confirm it is presented as {availability[adv]}")

    if offers is not None:
        odoc = sd.parse_document(offers, "offer-catalogue")
        ot = table(odoc, "Offers", "Status")
        if ot is not None:
            for i, r in enumerate(ot.rows):
                if sd.cell_text(r[ot.col("Status")]).lower() != "available":
                    continue
                cited = sorted(set(re.findall(r"\bADV-\d+\b", " ".join(r))) & not_current)
                for adv in cited:
                    add("review", "PLANNED-OFFER", offers, ot.line + 2 + i,
                        f"available offer {sd.cell_text(r[ot.col('ID')])} cites {adv}, whose capability is {availability[adv]}")
    return findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("differentiation", type=Path)
    c.add_argument("--positioning", type=Path)
    c.add_argument("--offers", type=Path)
    c.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    for p in (args.differentiation, args.positioning, args.offers):
        if p is not None and not p.is_file():
            print(f"cannot read {p}", file=sys.stderr)
            return 2
    try:
        findings = check(args.differentiation, args.positioning, args.offers)
    except (OSError, UnicodeDecodeError, IndexError) as e:
        print(f"cannot read documents: {e}", file=sys.stderr)
        return 2
    errors = [f for f in findings if f["level"] == "error"]
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for f in findings:
            print(f"{f['level']:7} {f['rule']:14} {f['path']}:{f['line']}  {f['message']}")
        print(f"{len(errors)} errors, {sum(f['level'] == 'review' for f in findings)} for review, "
              f"{sum(f['level'] == 'info' for f in findings)} info")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
