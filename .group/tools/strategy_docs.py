"""Read Strategy documents and contracts.

Shared by the group check, the group view and the members' tools. Pure functions over
text and paths: no writes, no network. The document rules these functions read are
defined in ../contracts/document-rules.md (§2 Basis); the type contracts declare sections
and columns. Basis markers in any row cell are available to the group check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

GROUP_DIR = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = GROUP_DIR / "contracts"

# type -> path pattern under venture/{v}/strategy/
TYPE_PATHS = {
    "venture-definition": "venture.md",
    "objectives": "objectives.md",
    "bet-portfolio": "bet-portfolio.md",
    "focus-plan": "focus-plan.md",
    "strategy-review": "strategy-review/*.md",
    "segments": "segments.md",
    "target-segments": "target-segments.md",
    "opportunities": "opportunities.md",
    "differentiation": "differentiation.md",
    "positioning-decision": "positioning-decision.md",
    "category-definition": "category-definition.md",
    "revenue-model": "revenue-model.md",
    "offer-catalogue": "offer-catalogue.md",
    "price-book": "price-book.md",
}

ORIGIN_RE = re.compile(r"\[(owner|observed|derived|estimate|proposed|accepted|hypothesis)\b[^\]]*\]", re.I)
OWNER_LABEL_RE = re.compile(r"\[owner\b([^\]]*)\]", re.I)
QUOTE_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
CURRENCY_CODES = r"USD|EUR|GBP|CHF|JPY|CAD|AUD|SEK|NOK|DKK|PLN|INR|SGD|NZD|BRL|MXN"
AMOUNT_RE = re.compile(
    rf"(?:(?:{CURRENCY_CODES})\s?\d[\d,]*(?:\.\d+)?\b|\b\d[\d,]*(?:\.\d+)?\s?(?:{CURRENCY_CODES})\b|[$€£]\s?\d[\d,]*(?:\.\d+)?)"
)
PERCENT_RE = re.compile(r"\b\d+(?:\.\d+)?\s?%")
HOURS_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:h|hrs?|hours?|person[- ]days?|person[- ]weeks?|FTEs?|days of (?:owner|founder) time)\b", re.I
)
ATTRIBUTION_PHRASE_RE = re.compile(
    r"\bowner[- ](?:stated|set|supplied|provided|specified|confirmed|given|defined|mandated|requested)\b"
    r"|\b(?:per|according to|as stated by) the owner\b"
    r"|\bthe owner(?:'s)? (?:said|says|stated|states|wants|wanted|asked|specified|confirmed|requires|required|decided)\b"
    r"|\bowner material (?:says|states|shows|confirms|specifies)\b"
    r"|\bowner's (?:brief|material|notes|words|statement)\b",
    re.I,
)
ID_RE = re.compile(r"\b([A-Z]{2,4})-(\d+)\b")
UNKNOWN_VALUES = {"unknown", "tbd", "?"}


@dataclass
class Table:
    headers: list[str]
    rows: list[list[str]]
    line: int  # 1-based line of the header row

    def col(self, name: str) -> int | None:
        for i, h in enumerate(self.headers):
            if norm_header(h) == norm_header(name):
                return i
        return None


@dataclass
class Section:
    name: str
    line: int
    text: str
    tables: list[Table] = field(default_factory=list)


@dataclass
class Document:
    path: Path
    type: str
    title: str | None
    owner_line: str | None
    built_from: str | None
    sections: list[Section]
    lines: list[str]

    def section(self, name: str) -> Section | None:
        for s in self.sections:
            if s.name.lower() == name.lower():
                return s
        return None


@dataclass
class ColumnSpec:
    name: str
    kind: str  # id | reasoning | factual | status | ref
    prefix: str | None = None
    values: list[str] = field(default_factory=list)
    ref_types: list[str] = field(default_factory=list)


@dataclass
class SectionSpec:
    name: str
    form: str
    required: bool
    condition: str | None
    columns: list[ColumnSpec] = field(default_factory=list)


@dataclass
class Contract:
    type: str
    sections: list[SectionSpec]

    def section(self, name: str) -> SectionSpec | None:
        for s in self.sections:
            if s.name.lower() == name.lower():
                return s
        return None

    def id_prefixes(self) -> list[str]:
        return [c.prefix for s in self.sections for c in s.columns if c.kind == "id" and c.prefix]


def norm_header(h: str) -> str:
    return strip_md(h).lower()


def strip_md(s: str) -> str:
    return s.replace("`", "").replace("**", "").strip()


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}", line)) and set(line.replace("|", "").replace(":", "").strip()) <= {"-", " "}


def parse_tables(lines: list[str], offset: int) -> list[Table]:
    tables: list[Table] = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            headers = split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append(Table(headers, rows, offset + i + 1))
            i = j
        else:
            i += 1
    return tables


def parse_document(path: Path, type_: str) -> Document:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = owner = built = None
    sections: list[Section] = []
    current: tuple[str, int, list[str]] | None = None
    start_line = 0

    def close(cur, start):
        if cur is None:
            return
        name, line, body = cur
        sections.append(Section(name, line, "\n".join(body), parse_tables(body, start)))

    for idx, raw in enumerate(lines):
        if raw.startswith("# ") and title is None and current is None:
            title = raw[2:].strip()
        elif raw.startswith("Owner:") and owner is None and current is None:
            owner = raw.strip()
        elif raw.startswith("Built from:") and built is None and current is None:
            built = raw[len("Built from:"):].strip()
        elif raw.startswith("## "):
            close(current, start_line)
            current = (raw[3:].strip(), idx + 1, [])
            start_line = idx + 1
        elif current is not None:
            current[2].append(raw)
    close(current, start_line)
    return Document(path, type_, title, owner, built, sections, lines)


def parse_contract(type_: str, contracts_dir: Path = CONTRACTS_DIR) -> Contract:
    text = (contracts_dir / f"{type_}.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    rep_start = next(i for i, l in enumerate(lines) if l.strip() == "## Representation")
    rep = lines[rep_start:]
    tables = parse_tables(rep, rep_start)
    sec_table = next(t for t in tables if t.col("Section") is not None and t.col("Requiredness") is not None)
    specs: list[SectionSpec] = []
    for row in sec_table.rows:
        name, form, req = strip_md(row[0]), row[sec_table.col("Form")], strip_md(row[sec_table.col("Requiredness")])
        required = req.lower().startswith("required")
        cond = req.split(":", 1)[1].strip() if req.lower().startswith("conditional") else None
        specs.append(SectionSpec(name, form, required, cond))
    # column tables follow "### {Section} columns"
    for i, l in enumerate(rep):
        m = re.match(r"^###\s+(.+?)\s+columns\s*$", l)
        if not m:
            continue
        spec = next((s for s in specs if s.name.lower() == m.group(1).lower()), None)
        if spec is None:
            raise ValueError(f"{type_}: columns for undeclared section {m.group(1)}")
        tbl = parse_tables(rep[i + 1:], rep_start + i + 1)[0]
        for row in tbl.rows:
            spec.columns.append(parse_kind(strip_md(row[0]), strip_md(row[tbl.col("Kind")])))
    return Contract(type_, specs)


def parse_kind(name: str, kind: str) -> ColumnSpec:
    k = kind.strip()
    if k.startswith("id "):
        return ColumnSpec(name, "id", prefix=k[3:].strip())
    if k.startswith("status:"):
        return ColumnSpec(name, "status", values=[v.strip().lower() for v in k[len("status:"):].split(",")])
    if k.startswith("ref "):
        return ColumnSpec(name, "ref", ref_types=[t.strip() for t in k[4:].split(" or ")])
    if k in ("reasoning", "factual"):
        return ColumnSpec(name, k)
    raise ValueError(f"unknown column kind {kind!r} for {name}")


def load_contracts(contracts_dir: Path = CONTRACTS_DIR) -> dict[str, Contract]:
    return {t: parse_contract(t, contracts_dir) for t in TYPE_PATHS}


def find_documents(strategy_dir: Path, overlay_candidates: bool = True) -> list[Document]:
    """Documents of the working view: current state with candidate/ laid over it."""
    docs: list[Document] = []
    for type_, pattern in TYPE_PATHS.items():
        current = {p.relative_to(strategy_dir): p for p in strategy_dir.glob(pattern)}
        if overlay_candidates and (strategy_dir / "candidate").is_dir():
            cand_root = strategy_dir / "candidate"
            for p in cand_root.glob(pattern):
                current[p.relative_to(cand_root)] = p
        for rel in sorted(current):
            docs.append(parse_document(current[rel], type_))
    return docs


def cell_text(cell: str) -> str:
    """Cell value without basis markers and markdown, for status and unit comparison."""
    return strip_md(ORIGIN_RE.sub("", cell)).strip()


def is_unknown(cell: str) -> bool:
    v = cell_text(cell).lower()
    return v in UNKNOWN_VALUES or v.startswith("unknown")


def is_na(cell: str) -> bool:
    return cell_text(cell).lower().startswith("n/a")


def ids_in(cell: str) -> list[str]:
    return [f"{m.group(1)}-{m.group(2)}" for m in ID_RE.finditer(strip_md(cell))]


def sentences(text: str) -> list[tuple[int, str]]:
    """Prose sentences with their line offset, skipping tables, headings and code."""
    out = []
    in_code = False
    for i, line in enumerate(text.splitlines()):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith("|") or line.startswith("#") or not line.strip():
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", line.strip()):
            out.append((i, s))
    return out


def owner_corpus(paths: list[Path]) -> str:
    """Normalised text of the owner material: files, or every text file under a directory."""
    texts = []
    for p in paths:
        files = [p] if p.is_file() else sorted(q for q in p.rglob("*") if q.is_file())
        for f in files:
            try:
                texts.append(f.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                continue
    return normalise("\n".join(texts))


def normalise(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[*_`>#]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def quote_present(quote: str, corpus: str) -> bool:
    parts = [normalise(p) for p in re.split(r"…|\.\.\.", quote) if p.strip()]
    pos = 0
    for part in parts:
        found = corpus.find(part, pos)
        if found < 0:
            return False
        pos = found + len(part)
    return bool(parts)
