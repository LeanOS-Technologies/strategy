"""Product-local, standard-library support for contained result readers."""
import base64
import hashlib
import json
import mimetypes
import os
import shutil
import subprocess
import webbrowser
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent

def payload(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")

def data_url(path):
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode()

def styles():
    assets = HERE / "reader-assets"
    css = (assets / "tokens.css").read_text()
    for font in (assets / "fonts").glob("*.woff2"):
        css = css.replace("fonts/" + font.name, data_url(font))
    return css + "\n" + (HERE / ("reader.css" if (HERE / "reader.css").exists() else "result.css")).read_text()

def shell(product, title, lead, body, data, script, *, note="", view_type="result", extra_css=""):
    licences = "\n\n".join(p.name + "\n" + p.read_text() for p in sorted((HERE / "reader-assets/fonts").glob("LICENSE-*.txt")))
    is_tool = view_type == "tool"
    if is_tool:
        licences = "\n".join(line.rstrip() for line in licences.split("\n"))
    skip = "Skip to tool guide" if is_tool else "Skip to result"
    label = "Tool guide" if is_tool else "Your result"
    footer = "Definitions and mechanics of the tool." if is_tool else "Source meaning and recorded evidence status are preserved. The choice remains yours."
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            + "<title>" + escape(title) + " · " + escape(product) + "</title><style>" + styles() + extra_css + "</style></head><body>"
            + '<a class="skip" href="#main">' + skip + '</a><header class="masthead"><span class="wordmark">' + escape(product) + '<span>.</span></span><nav aria-label="View controls"><button class="theme-control" id="theme" type="button">Switch to dark</button></nav></header>'
            + '<main id="main"><div class="intro"><p class="eyebrow">' + escape(product) + ' · ' + label + '</p><h1>' + escape(title) + '</h1><p class="lead">' + escape(lead) + '</p></div>' + (('<p class="reading-note">'+escape(note)+'</p>') if note else '') + body
            + '<noscript><p>JavaScript enables search and navigation. The result content is available below.</p></noscript></main><footer>' + escape(product) + ' · ' + footer + '<details><summary>Font licences</summary><pre>' + escape(licences) + '</pre></details></footer>'
            + '<script id="result-data" type="application/json">' + payload(data) + '</script><script>'
            + "document.getElementById('theme').onclick=()=>{const d=document.documentElement;d.dataset.theme=d.dataset.theme==='dark'?'light':'dark';document.getElementById('theme').textContent=d.dataset.theme==='dark'?'Switch to light':'Switch to dark';};" + script + '</script></body></html>')

def open_result(path):
    path = path.resolve()
    try:
        opener = shutil.which("wslview") if os.environ.get("WSL_DISTRO_NAME") else None
        opened = (subprocess.run([opener, str(path)], capture_output=True, timeout=15).returncode == 0) if opener else webbrowser.open(path.as_uri(), new=2)
    except (OSError, subprocess.TimeoutExpired, webbrowser.Error):
        opened = False
    print(("Browser open requested: " if opened else "Browser unavailable; open this result: ") + str(path))
    return opened


def tool_shell(product, title, lead, body, data=None, script=""):
    """Tool mechanics and produced results share the same local shell and design tokens."""
    controls = '<nav id="tool-nav" class="chapter-nav tool-nav" aria-label="Tool sections"></nav><form class="toolbar" role="search"><label>Find a definition or capability<input id="tool-search" type="search" placeholder="Search the tool guide"></label><button class="quiet" type="reset">Clear search</button></form><p id="tool-status" role="status"></p>'
    body = controls + '<div class="tool-content">' + body + '</div>'
    return shell(product, title, lead, body, data or {"product":product,"view":"tool"}, (HERE / "tool.js").read_text() + script, view_type="tool", extra_css=(HERE / "tool.css").read_text())


def output_files(paths):
    """One actual output filename/pattern per line, shared by every tool guide."""
    return '<div class="member-outputs"><h4>Writes files</h4><ul class="file-list">'+''.join('<li><code class="file-name">'+escape(path)+'</code></li>' for path in paths)+'</ul></div>'


def atlas_skills(root):
    """Declare the installed skills using their existing names and descriptions."""
    import re
    cards=[]
    for path in sorted((Path(root)/'.claude/skills').glob('*/SKILL.md')):
        source=path.read_text();name=re.search(r'^name:\s*(.+)$',source,re.M);description=re.search(r'^description:\s*(.+)$',source,re.M)
        title=name[1].strip() if name else path.parent.name
        text=description[1].strip().strip('"') if description else ''
        cards.append('<article class="card"><h3><code class="chip">'+escape(title)+'</code></h3><p>'+escape(text)+'</p></article>')
    return '<h2 id="skills">Skills</h2><div class="grid atlas-skills">'+''.join(cards)+'</div>'
