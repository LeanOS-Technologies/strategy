#!/usr/bin/env python3
"""Generate the Strategy group view from its definition files.

Usage:
  python3 view.py            write ../view/index.html
  python3 view.py --check    exit 1 when ../view/index.html differs from what the files generate

Reads AGENTS.md, .group/contracts/*.md and each member's skills. Deterministic: the same
files give the same page. Writes only ../view/index.html.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strategy_docs as sd  # noqa: E402

GROUP_ROOT = sd.GROUP_DIR.parent
VIEW = sd.GROUP_DIR / "view" / "index.html"

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#5d5b55;--line:#dedad0;--accent:#2f5d50;--chip:#eef2ee}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#ecebe6;--muted:#a7a49b;--line:#34332f;--accent:#8cc3b0;--chip:#1f2a26}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1080px;margin:0 auto;padding:32px 16px 64px}h1{font-size:28px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
h3{font-size:16px;margin:20px 0 6px}p{margin:6px 0}.muted{color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:8px 0 14px;font-size:14px}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--chip)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.chip{display:inline-block;background:var(--chip);border-radius:4px;padding:1px 6px;margin:2px 4px 2px 0;font-size:13px}code{font-size:13px}
details{border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:8px 0}summary{cursor:pointer;font-weight:600}
.wrap{overflow-x:auto}
"""


def esc(s: str) -> str:
    s = html.escape(sd.strip_md(s) if s.startswith("`") else s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.replace("**", "")


def table_html(t: sd.Table) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in t.headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t.rows)
    return f'<div class="wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def section_tables(md: str, heading: str) -> list[sd.Table]:
    lines = md.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == f"## {heading}")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return sd.parse_tables(lines[start + 1:end], start + 1)


def first_paragraph(md: str, heading: str) -> str:
    lines = md.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == f"## {heading}")
    para = []
    for l in lines[start + 1:]:
        if l.startswith("## "):
            break
        if not l.strip():
            if para:
                break
            continue
        para.append(l.strip())
    return " ".join(para)


def skill_info(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    name = re.search(r"^name:\s*(.+)$", text, re.M)
    desc = re.search(r"^description:\s*(.+)$", text, re.M)
    return (name.group(1).strip() if name else path.parent.name, desc.group(1).strip().strip('"') if desc else "")


def build() -> str:
    agents = (GROUP_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    identity = section_tables(agents, "Identity")[0]
    state = next(r[1] for r in identity.rows if sd.strip_md(r[0]) == "State")
    members = section_tables(agents, "Members")[0]
    parts = [f"<h1>Strategy</h1><p class='muted'>{esc(state)}</p>"]
    parts.append("<p class='muted'>Generated from AGENTS.md, .group/contracts and the members' skills. Never edited.</p>")

    parts.append("<h2>Members and skills</h2><div class='grid'>")
    for row in members.rows:
        member = sd.strip_md(row[0])
        skills_dir = GROUP_ROOT / member / ".claude" / "skills"
        skills = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
        items = "".join(f"<p><span class='chip'>{esc(n)}</span> {esc(d)}</p>" for n, d in map(skill_info, skills))
        parts.append(f"<div class='card'><h3>{esc(member)}</h3><p class='muted'>{esc(row[2])}</p>{items}</div>")
    parts.append("</div>")

    parts.append("<h2>Must-agree rules</h2>")
    parts.extend(table_html(t) for t in section_tables(agents, "Must-agree rules"))
    parts.append("<h2>Routing</h2>")
    parts.extend(table_html(t) for t in section_tables(agents, "Routing"))

    parts.append("<h2>Contracts</h2>")
    for type_ in sd.TYPE_PATHS:
        md = (sd.CONTRACTS_DIR / f"{type_}.md").read_text(encoding="utf-8")
        contract = sd.parse_contract(type_)
        rows = "".join(
            f"<tr><td>{esc(s.name)}</td><td>{esc(s.form)}</td><td>{'required' if s.required else 'when ' + esc(s.condition or '')}</td>"
            f"<td>{', '.join(esc(c.name) for c in s.columns)}</td></tr>"
            for s in contract.sections
        )
        parts.append(
            f"<details><summary>{esc(type_)} <span class='muted'>· venture/{{v}}/strategy/{esc(sd.TYPE_PATHS[type_])}</span></summary>"
            f"<p>{esc(first_paragraph(md, 'Meaning'))}</p>"
            f"<div class='wrap'><table><thead><tr><th>Section</th><th>Form</th><th>Requiredness</th><th>Columns</th></tr></thead><tbody>{rows}</tbody></table></div></details>"
        )
    parts.append("<h2>Boundary</h2>")
    parts.extend(table_html(t) for t in section_tables(agents, "Boundary"))
    body = "\n".join(parts)
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>Strategy group</title><style>{CSS}</style></head><body><main>\n{body}\n</main></body></html>\n"
    )


def main(argv: list[str]) -> int:
    page = build()
    if "--check" in argv:
        current = VIEW.read_text(encoding="utf-8") if VIEW.exists() else ""
        if current != page:
            print("group view is stale: run python3 view.py")
            return 1
        print("group view is current")
        return 0
    VIEW.parent.mkdir(parents=True, exist_ok=True)
    VIEW.write_text(page, encoding="utf-8")
    print(f"wrote {VIEW}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
