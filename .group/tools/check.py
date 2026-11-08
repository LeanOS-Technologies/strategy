#!/usr/bin/env python3
"""Check Strategy documents against their contracts and the group's machine-checkable rules.

Usage:
  python3 check.py STRATEGY_DIR [--owner-material PATH ...] [--no-candidates] [--json]

STRATEGY_DIR is venture/{v}/strategy (or any directory with the same layout). The working
view is current state with candidate/ laid over it, unless --no-candidates.
--owner-material names the owner material (files or directories) that [owner: "…"] quotes
must appear in; without it, quotes are reported unchecked.

Read-only and deterministic: the same files give the same findings. Exit 0 when no finding
has level error, 1 otherwise, 2 on a usage or contract-parse failure.

Rules (document-rules.md §2 Basis and AGENTS.md must-agree):
  ENVELOPE  title, Owner line, Built from line, Conclusion first
  SECTION   required sections present or "Omitted: reason"; conditional ones optional
  COLUMN    declared columns present in each table section
  STATUS    status cells hold a declared value
  REASONING reasoning cells are filled with reasoning, never "unknown"
  ID        ids carry the type's prefix and are unique in the document
  REF       references name records of the declared type
  NUM-BASIS every amount or percentage carries its basis in the row (including a basis or source cell) or sentence
  ATTRIB-QUOTE   an [owner] label quotes a passage
  ATTRIB-ABSENT  the quoted passage appears in the owner material
  ATTRIB-PHRASE  an attribution phrase carries an [owner: "…"] label beside it
  ARITH     "{expression} = {result}" holds and its units are compatible
  CIRCULAR  an [observed: …] label never cites a Strategy document
  FOCUS-MONEY focus-plan holds no amount of money and no hour or headcount estimate
  PRICED    every offer has a price row
  UNIT      a price's charging unit matches its offer's revenue-model exchange

A factual value that is unknown or inapplicable never produces a finding.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strategy_docs as sd  # noqa: E402


@dataclass
class Finding:
    level: str  # error | unchecked
    rule: str
    path: str
    line: int
    message: str


class Checker:
    def __init__(self, root: Path, contracts: dict[str, sd.Contract], corpus: str | None):
        self.root = root
        self.contracts = contracts
        self.corpus = corpus
        self.findings: list[Finding] = []

    def add(self, level, rule, doc, line, msg):
        try:
            rel = str(doc.path.relative_to(self.root))
        except ValueError:
            rel = str(doc.path)
        self.findings.append(Finding(level, rule, rel, line, msg))

    # ---- per document -------------------------------------------------
    def check_document(self, doc: sd.Document, ids_by_type: dict[str, set[str]]):
        c = self.contracts[doc.type]
        self.check_envelope(doc)
        order = []
        for spec in c.sections:
            sec = doc.section(spec.name)
            if sec is None:
                if spec.required:
                    self.add("error", "SECTION", doc, 1, f"required section '{spec.name}' is missing; add it or write 'Omitted: {{reason}}' under it")
                continue
            order.append(doc.sections.index(sec))
            if sec.text.strip().lower().startswith("omitted:"):
                continue
            if spec.columns:
                self.check_table_section(doc, spec, sec, ids_by_type)
        if order != sorted(order):
            self.add("error", "SECTION", doc, 1, "sections are out of contract order")
        self.check_text_rules(doc)
        if doc.type == "focus-plan":
            self.check_focus_money(doc)

    def check_envelope(self, doc):
        if not doc.title:
            self.add("error", "ENVELOPE", doc, 1, "missing '# Title'")
        if not doc.owner_line or not re.match(r"^Owner: [\w-]+/[\w-]+ · Updated: \d{4}-\d{2}-\d{2}$", doc.owner_line):
            self.add("error", "ENVELOPE", doc, 1, "Owner line must read 'Owner: {worker}/{skill} · Updated: YYYY-MM-DD'")
        if doc.built_from is None:
            self.add("error", "ENVELOPE", doc, 1, "missing 'Built from:' line")
        if not doc.sections or doc.sections[0].name != "Conclusion" or not doc.sections[0].text.strip():
            self.add("error", "ENVELOPE", doc, 1, "the first section must be a non-empty '## Conclusion'")

    def check_table_section(self, doc, spec, sec, ids_by_type):
        table = next((t for t in sec.tables if all(t.col(col.name) is not None for col in spec.columns)), None)
        if table is None:
            have = sec.tables[0].headers if sec.tables else []
            missing = [col.name for col in spec.columns if not sec.tables or sec.tables[0].col(col.name) is None]
            self.add("error", "COLUMN", doc, sec.line, f"section '{spec.name}' needs a table with columns {missing} (found {have})")
            return
        seen: set[str] = set()
        for r, row in enumerate(table.rows):
            line = table.line + 2 + r
            for col in spec.columns:
                i = table.col(col.name)
                cell = row[i] if i < len(row) else ""
                self.check_cell(doc, spec, col, cell, line, seen, ids_by_type)

    def check_cell(self, doc, spec, col, cell, line, seen, ids_by_type):
        value = sd.cell_text(cell)
        if col.kind == "id":
            if not re.fullmatch(rf"{col.prefix}-\d+", value):
                self.add("error", "ID", doc, line, f"'{col.name}' must be an id {col.prefix}-n, found '{value}'")
            elif value in seen:
                self.add("error", "ID", doc, line, f"duplicate id {value}")
            seen.add(value)
        elif col.kind == "status":
            if value.lower() not in col.values:
                self.add("error", "STATUS", doc, line, f"'{col.name}' must be one of {col.values}, found '{value}'")
        elif col.kind == "reasoning":
            # a label that names its quote, method or reference is a basis; a bare [proposed] is not reasoning
            substantive_label = re.search(r"\[(owner|observed|derived|estimate):\s*[^\]]+\]", cell, re.I)
            if (not value and not substantive_label) or value.lower() in sd.UNKNOWN_VALUES:
                self.add("error", "REASONING", doc, line, f"'{col.name}' carries required reasoning; write the {col.name.lower()}")
        elif col.kind == "ref":
            if not value or value.lower() in ("none", "n/a") or sd.is_na(cell):
                return
            refs = sd.ids_in(cell)
            if not refs:
                self.add("error", "REF", doc, line, f"'{col.name}' must reference {' or '.join(col.ref_types)} ids, found '{value}'")
                return
            pools = [ids_by_type.get(t) for t in col.ref_types]
            if all(p is None for p in pools):
                self.add("unchecked", "REF", doc, line, f"'{col.name}' references {refs}; no {' or '.join(col.ref_types)} document in the set")
                return
            known = set().union(*[p for p in pools if p is not None])
            for ref in refs:
                if ref not in known:
                    self.add("error", "REF", doc, line, f"'{col.name}' references {ref}, which no {' or '.join(col.ref_types)} record declares")

    # ---- text rules: labels, attribution, arithmetic ---------------------
    def units(self, doc):
        """Rows of every table and sentences of prose, with line numbers."""
        for sec in doc.sections:
            for t in sec.tables:
                for r, row in enumerate(t.rows):
                    yield t.line + 2 + r, " | ".join(row)
            for off, s in sd.sentences(sec.text):
                yield sec.line + 1 + off, s
        if doc.title:
            yield 1, doc.title

    def check_text_rules(self, doc):
        for line, text in self.units(doc):
            labelled = bool(sd.ORIGIN_RE.search(text))
            if (sd.AMOUNT_RE.search(text) or sd.PERCENT_RE.search(text)) and not labelled:
                self.add("error", "NUM-BASIS", doc, line, f"amount or percentage without basis in its row or sentence: '{short(text)}'")
            owner_quotes = []
            for m in sd.OWNER_LABEL_RE.finditer(text):
                q = sd.QUOTE_RE.search(m.group(1))
                if not q:
                    self.add("error", "ATTRIB-QUOTE", doc, line, f"owner attribution without a quoted passage: '{short(m.group(0))}'")
                    continue
                owner_quotes.append(q.group(1))
            if sd.ATTRIBUTION_PHRASE_RE.search(text) and not owner_quotes:
                self.add("error", "ATTRIB-PHRASE", doc, line, f"attribution to the owner without an [owner: \"…\"] quote: '{short(text)}'")
            for q in owner_quotes:
                if self.corpus is None:
                    self.add("unchecked", "ATTRIB-ABSENT", doc, line, f"quote not checked (no --owner-material): \"{short(q)}\"")
                elif not sd.quote_present(q, self.corpus):
                    self.add("error", "ATTRIB-ABSENT", doc, line, f"quoted passage is not in the owner material: \"{short(q)}\"")
            for m in re.finditer(r"\[observed:\s*([^\]]+)\]", text, re.I):
                ref = m.group(1).strip().lstrip("/")
                kind = ref.split("/")[0] if not ref.startswith("strategy/") else ref.split("/")[1]
                kind = re.sub(r"\.md.*$|#.*$|/.*$", "", kind)
                if ref.startswith("strategy/") or kind in sd.TYPE_PATHS or kind == "venture":
                    self.add("error", "CIRCULAR", doc, line, f"'{short(m.group(0))}' cites a Strategy document as an observation; cite the observation it rests on, or label the statement derived, proposed or hypothesis")
            for problem in arithmetic_problems(text):
                self.add("error", "ARITH", doc, line, problem)

    def check_focus_money(self, doc):
        for line, text in self.units(doc):
            for rx, what in ((sd.AMOUNT_RE, "an amount of money"), (sd.HOURS_RE, "an hour or headcount estimate")):
                m = rx.search(text)
                if m:
                    self.add("error", "FOCUS-MONEY", doc, line, f"focus-plan holds {what} ('{m.group(0)}'); name the purchase and the action that needs it, and leave amounts to Finance")

    # ---- cross-document -------------------------------------------------
    def check_set(self, docs):
        by_type = {d.type: d for d in docs}
        offers = by_type.get("offer-catalogue")
        prices = by_type.get("price-book")
        model = by_type.get("revenue-model")
        if offers and prices:
            ot = table_of(offers, "Offers", "ID")
            pt = table_of(prices, "Prices", "Offer")
            if ot and pt:
                priced = {ref for row in pt.rows for ref in sd.ids_in(row[pt.col("Offer")])}
                for r, row in enumerate(ot.rows):
                    oid = sd.cell_text(row[ot.col("ID")])
                    if oid not in priced:
                        self.add("error", "PRICED", offers, ot.line + 2 + r, f"{oid} has no row in price-book Prices; give a price, 'free', or 'unknown' with the deciding question")
        if offers and prices and model:
            ot = table_of(offers, "Offers", "Revenue model")
            pt = table_of(prices, "Prices", "Charging unit")
            mt = table_of(model, "Charging mechanics", "Charging unit")
            if ot and pt and mt:
                units_by_model: dict[str, set[str]] = {}
                for row in mt.rows:
                    for mid in sd.ids_in(row[mt.col("Model")]):
                        units_by_model.setdefault(mid, set()).add(unit_key(row[mt.col("Charging unit")]))
                model_of_offer = {sd.cell_text(row[ot.col("ID")]): sd.ids_in(row[ot.col("Revenue model")]) for row in ot.rows}
                for r, row in enumerate(pt.rows):
                    unit = unit_key(row[pt.col("Charging unit")])
                    if unit in ("", "unknown", "n/a") or unit.startswith("n/a"):
                        continue
                    for oid in sd.ids_in(row[pt.col("Offer")]):
                        allowed = set().union(*[units_by_model.get(m, set()) for m in model_of_offer.get(oid, [])] or [set()])
                        if allowed and unit not in allowed:
                            self.add("error", "UNIT", prices, pt.line + 2 + r, f"{oid} is priced per '{unit}', but its revenue-model exchange charges per {sorted(allowed)}")


def table_of(doc, section, column):
    sec = doc.section(section)
    if not sec:
        return None
    return next((t for t in sec.tables if t.col(column) is not None), None)


def unit_key(cell: str) -> str:
    return re.sub(r"\s+", " ", sd.cell_text(cell).lower()).strip()


def short(s: str, n: int = 90) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


# ---- arithmetic -----------------------------------------------------------
NUM = r"\d[\d,]*(?:\.\d+)?"
CUR = sd.CURRENCY_CODES
TERM = rf"(?:[$€£]\s?{NUM}|(?:{CUR})\s?{NUM}|{NUM}(?:\s?%|\s?(?:{CUR})\b|\s[a-z][a-z-]*\b)?)"
OP = r"\s*[+\-−×*/÷]\s*"
CALC_RE = re.compile(rf"({TERM}(?:{OP}{TERM})+)\s*=\s*({TERM})")
SYMBOLS = {"$": "USD", "€": "EUR", "£": "GBP"}


def parse_term(t: str):
    t = t.strip()
    for sym, code in SYMBOLS.items():
        if t.startswith(sym):
            return float(t[1:].replace(",", "").strip()), {code: 1}, decimals(t)
    m = re.match(rf"^({CUR})\s?({NUM})$", t)
    if m:
        return float(m.group(2).replace(",", "")), {m.group(1): 1}, decimals(m.group(2))
    m = re.match(rf"^({NUM})\s?(%|{CUR}|[a-z][a-z-]*)?$", t)
    if not m:
        raise ValueError(t)
    value = float(m.group(1).replace(",", ""))
    unit = m.group(2)
    if unit == "%":
        return value / 100, {}, decimals(m.group(1)) + 2
    if unit is None:
        return value, {}, decimals(m.group(1))
    return value, {unit.rstrip("s") if not re.fullmatch(CUR, unit) else unit: 1}, decimals(m.group(1))


def decimals(s: str) -> int:
    m = re.search(r"\.(\d+)", s)
    return len(m.group(1)) if m else 0


def currencies(u: dict) -> set:
    return {k for k, v in u.items() if re.fullmatch(CUR, k) and v != 0}


def arithmetic_problems(text: str) -> list[str]:
    problems = []
    for m in CALC_RE.finditer(text):
        expr, result = m.group(1), m.group(2)
        tokens = re.split(rf"({OP})", expr)
        terms = [parse_term(x) for x in tokens[0::2]]
        ops = [x.strip() for x in tokens[1::2]]
        # additive groups of multiplicative products
        groups, cur = [], [terms[0]]
        cur_ops = []
        for op, term in zip(ops, terms[1:]):
            if op in "+-−":
                groups.append((cur, cur_ops))
                groups.append(op)
                cur, cur_ops = [term], []
            else:
                cur.append(term)
                cur_ops.append(op)
        groups.append((cur, cur_ops))
        total, total_unit, sign, unit_error = 0.0, None, 1, None
        for g in groups:
            if isinstance(g, str):
                sign = 1 if g == "+" else -1
                continue
            factors, fops = g
            value, unit = factors[0][0], dict(factors[0][1])
            for op, (v, u, _) in zip(fops, factors[1:]):
                if op in "×*":
                    value *= v
                    for k, e in u.items():
                        unit[k] = unit.get(k, 0) + e
                else:
                    if v == 0:
                        unit_error = "division by zero"
                        break
                    value /= v
                    for k, e in u.items():
                        unit[k] = unit.get(k, 0) - e
            unit = {k: e for k, e in unit.items() if e != 0}
            if len(currencies(unit)) > 1 or any(unit.get(c, 0) not in (0, 1, -1) for c in currencies(unit)):
                unit_error = f"incompatible currencies in '{short(expr, 50)}'"
            if total_unit is None:
                total_unit = unit
            elif currencies(total_unit) != currencies(unit):
                unit_error = f"adds terms with different units in '{short(expr, 50)}'"
            total += sign * value
        rv, ru, rdec = parse_term(result)
        if unit_error:
            problems.append(unit_error)
            continue
        if currencies(ru) != currencies(total_unit or {}):
            problems.append(f"result unit {sorted(currencies(ru)) or 'none'} differs from expression unit {sorted(currencies(total_unit or {})) or 'none'} in '{short(m.group(0), 60)}'")
            continue
        tolerance = max(0.5 * 10 ** (-rdec), 0.005 * abs(rv))
        if abs(total - rv) > tolerance + 1e-9:
            problems.append(f"'{short(m.group(0), 60)}' does not hold: the expression gives {round(total, rdec + 2)}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("strategy_dir", type=Path)
    ap.add_argument("--owner-material", type=Path, nargs="*", default=None)
    ap.add_argument("--no-candidates", action="store_true")
    ap.add_argument("--contracts", type=Path, default=sd.CONTRACTS_DIR)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if not args.strategy_dir.is_dir():
        print(f"not a directory: {args.strategy_dir}", file=sys.stderr)
        return 2
    try:
        contracts = sd.load_contracts(args.contracts)
    except Exception as e:  # contract parse failure is a defect in the contract
        print(f"contract parse failure: {e}", file=sys.stderr)
        return 2
    corpus = sd.owner_corpus(args.owner_material) if args.owner_material else None
    docs = sd.find_documents(args.strategy_dir, overlay_candidates=not args.no_candidates)
    checker = Checker(args.strategy_dir, contracts, corpus)
    ids_by_type: dict[str, set[str]] = {}
    for d in docs:
        for spec in contracts[d.type].sections:
            for col in spec.columns:
                if col.kind != "id":
                    continue
                t = table_of(d, spec.name, col.name)
                if t:
                    ids_by_type.setdefault(d.type, set()).update(sd.cell_text(r[t.col(col.name)]) for r in t.rows)
        ids_by_type.setdefault(d.type, set())
    for d in docs:
        checker.check_document(d, ids_by_type)
    checker.check_set(docs)
    errors = [f for f in checker.findings if f.level == "error"]
    if args.json:
        print(json.dumps({"documents": [str(d.path.relative_to(args.strategy_dir)) for d in docs],
                          "findings": [asdict(f) for f in checker.findings]}, indent=2))
    else:
        print(f"checked {len(docs)} documents in {args.strategy_dir}")
        for f in checker.findings:
            print(f"{f.level:9} {f.rule:13} {f.path}:{f.line}  {f.message}")
        print(f"{len(errors)} errors, {len(checker.findings) - len(errors)} unchecked")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
