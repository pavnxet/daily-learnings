#!/usr/bin/env python3
"""Build docs/ for GitHub Pages from tools/*.md.

GitHub Pages serves .md as plain text, so each entry gets a styled HTML page and
docs/index.html is rebuilt from the entries themselves -- nothing to hand-maintain.

Pages must be published from the /docs folder on main.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "tools"
OUT = ROOT / "docs"
REPO = "https://github.com/pavnxet/daily-learnings"
SITE = "https://pavnxet.github.io/daily-learnings"

# Safety net for entries with no "- **Logged**:" line.
DEFAULT_DATE = "2026-10-10"

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{ --bg:#fff; --fg:#1a1a1a; --muted:#6b6b6b; --rule:#e6e6e6; --link:#0b5cad; --card:#fafafa; }
@media (prefers-color-scheme:dark){
  :root{ --bg:#141414; --fg:#e8e8e8; --muted:#9a9a9a; --rule:#2e2e2e; --link:#6fb3ff; --card:#1c1c1c; }
}
/* explicit choice beats the system preference; equal specificity, so these must come after */
[data-theme=light]{ --bg:#fff; --fg:#1a1a1a; --muted:#6b6b6b; --rule:#e6e6e6; --link:#0b5cad; --card:#fafafa; }
[data-theme=dark]{ --bg:#141414; --fg:#e8e8e8; --muted:#9a9a9a; --rule:#2e2e2e; --link:#6fb3ff; --card:#1c1c1c; }
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
.theme-toggle{position:fixed;top:1rem;right:1rem;z-index:10;cursor:pointer;
  font:inherit;font-size:.8rem;line-height:1;padding:.5rem .75rem;border-radius:999px;
  color:var(--muted);background:var(--card);border:1px solid var(--rule)}
.theme-toggle:hover{color:var(--fg);border-color:var(--link)}
.theme-toggle:focus-visible{outline:2px solid var(--link);outline-offset:2px}
@media print{.theme-toggle{display:none}}
.wrap{max-width:46rem;margin:0 auto;padding:3.5rem 1.25rem 5rem}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
header.site{margin-bottom:2.5rem}
header.site h1{font-size:1.9rem;line-height:1.2;margin:0 0 .5rem;letter-spacing:-.02em}
header.site p{color:var(--muted);margin:0}
header.site nav{margin-top:1rem;font-size:.9rem;color:var(--muted)}
header.site nav a{margin-right:1rem}
h2{font-size:1.05rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);
   font-weight:600;margin:2.5rem 0 1rem;padding-bottom:.4rem;border-bottom:1px solid var(--rule)}
h3{font-size:1.15rem;margin:2rem 0 .5rem}
/* entry pages: the first section heading already sits next to the page title */
.entry>h2:first-child{font-size:1.15rem;letter-spacing:normal;text-transform:none;
  color:var(--fg);margin-top:0;border-bottom:0;padding-bottom:0}
ul,ol{padding-left:1.3rem}
li{margin:.35rem 0}
code{font:.88em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
     background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:.1em .35em}
pre{background:var(--card);border:1px solid var(--rule);border-radius:8px;
    padding:1rem;overflow-x:auto}
pre code{background:none;border:0;padding:0;font-size:.85rem;line-height:1.5}
table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.93rem}
th,td{border:1px solid var(--rule);padding:.5rem .7rem;text-align:left;vertical-align:top}
th{background:var(--card);font-weight:600}
blockquote{margin:1rem 0;padding-left:1rem;border-left:3px solid var(--rule);color:var(--muted)}
hr{border:0;border-top:1px solid var(--rule);margin:2.5rem 0}
/* index cards */
.card{display:block;padding:1.1rem 1.2rem;margin:.9rem 0;border:1px solid var(--rule);
      border-radius:10px;background:var(--card);color:inherit}
.card:hover{border-color:var(--link);text-decoration:none}
.card .t{font-weight:600;font-size:1.05rem}
.card .d{color:var(--muted);font-size:.94rem;margin:.35rem 0 0}
.card .m{color:var(--muted);font-size:.8rem;margin-top:.6rem;
         font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.empty{color:var(--muted);font-style:italic}
footer.site{margin-top:4rem;padding-top:1.5rem;border-top:1px solid var(--rule);
            color:var(--muted);font-size:.88rem}
.page-head{margin-bottom:2rem}
.page-head h1{font-size:1.7rem;line-height:1.25;margin:0 0 .4rem;letter-spacing:-.02em}
.page-head .m{margin:0}
.langs{margin:.5rem 0 0;font-size:.9rem;color:var(--muted)}
.langs strong{color:var(--fg)}
.back{font-size:.88rem}
"""

# Runs before the stylesheet so a saved theme never flashes the wrong colours first.
THEME_INIT = """
try{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}catch(e){}
"""

# Two-state toggle; the icon shows the theme you would switch to.
THEME_JS = """
(function(){
  var root=document.documentElement, btn=document.getElementById('theme-toggle');
  function isDark(){
    var t=root.dataset.theme;
    if(t) return t==='dark';
    return matchMedia('(prefers-color-scheme:dark)').matches;
  }
  function label(){
    var dark=isDark();
    btn.textContent=dark? '\\u2600 Light':'\\u263D Dark';
    btn.setAttribute('aria-label','Switch to '+(dark?'light':'dark')+' theme');
  }
  btn.addEventListener('click',function(){
    var next=isDark()? 'light':'dark';
    root.dataset.theme=next;
    try{localStorage.setItem('theme',next)}catch(e){}
    label();
  });
  matchMedia('(prefers-color-scheme:dark)').addEventListener('change',label);
  label();
})();
"""

INLINE = [
    (re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])"), r"<em>\1</em>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\((vendor claim[^)]*)\)"), r"<strong>(\1)</strong>"),
]


def inline(text):
    """Escape first, then apply inline markdown so entities survive."""
    out = html.escape(text, quote=False)
    for pattern, repl in INLINE:
        out = pattern.sub(repl, out)
    return out


def split_row(line):
    """Split a markdown table row on unescaped pipes."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def is_divider(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def collect_table(lines, i):
    """Read a pipe table starting at lines[i]; return (html, next_index)."""
    header = split_row(lines[i])
    body = []
    i += 1
    if i < len(lines) and is_divider(split_row(lines[i])):
        i += 1
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        body.append(split_row(lines[i]))
        i += 1
    head = "".join(f"<th>{inline(c)}</th>" for c in header)
    rows = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in body
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>", i


def convert(md):
    """Minimal markdown subset: headings, fenced code, tables, lists, quotes, hr."""
    lines = md.split("\n")
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            continue

        if stripped.startswith("|"):
            flush()
            table, i = collect_table(lines, i)
            out.append(table)
            continue

        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flush()
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            flush()
            level = min(len(heading.group(1)), 6)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        bullet = re.match(r"[-*]\s+(.*)", stripped)
        if bullet:
            flush()
            items = []
            while i < len(lines):
                m = re.match(r"[-*]\s+(.*)", lines[i].strip())
                if not m:
                    break
                items.append(f"<li>{inline(m.group(1))}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        numbered = re.match(r"\d+\.\s+(.*)", stripped)
        if numbered:
            flush()
            items = []
            while i < len(lines):
                m = re.match(r"\d+\.\s+(.*)", lines[i].strip())
                if not m:
                    break
                items.append(f"<li>{inline(m.group(1))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        if stripped.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue

        if not stripped:
            flush()
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush()
    return "\n".join(out)


def field(md, name, default=""):
    m = re.search(rf"^-\s+\*\*{name}\*\*:\s*(.+)$", md, re.M)
    return m.group(1).strip() if m else default


def strip_vendor_tags(text):
    """'X (vendor claim - unverified), Y (vendor claim - unverified)' -> 'X, Y'."""
    return re.sub(r"\s*\(vendor claim[^)]*\)", "", text).strip().rstrip(",.;:")


def ref_link(md, name):
    """Resolve a reference-style definition, e.g. '[PyPI]: https://...'."""
    m = re.search(rf"^\[{re.escape(name)}\]:\s*(\S+)", md, re.M)
    return m.group(1) if m else ""


def body_of(md):
    """Drop the title and metadata block, normalise link syntax, keep the sections."""
    lines = md.split("\n")
    start = 0
    for n, line in enumerate(lines):
        if line.startswith("## "):
            start = n
            break
    text = "\n".join(lines[start:])
    # Sources entries written as bare URLs would render as unlinked text.
    text = re.sub(r"^(https?://\S+)$", r"[\1](\1)", text, flags=re.M)
    text = re.sub(r"^-\s+(https?://\S+)$", r"- [\1](\1)", text, flags=re.M)
    # Normalise the vendor-claim tag first, so the generator's own matcher and
    # hand-written variants all end up identical in the output.
    text = re.sub(r"\(\s*vendor claims?\b[^)]*\)", "(vendor claim — unverified)", text)
    text = re.sub(r"\[\[([^\]]+)\]\]\(([^)]+)\)", r"[\1](\2)", text)
    text = re.sub(r"\[([^\]]+)\]\[([^\]]+)\]", lambda m: ref_link(text, m.group(2)) or m.group(1), text)
    text = re.sub(r"^\[([^\]]+)\]:\s*\S+\s*$", "", text, flags=re.M)
    return text


# --- translations -----------------------------------------------------------
# Entries are authored in English (tools/<slug>.md). A translation is an optional
# companion file (tools/<slug>.<lang>.md) holding a full translated page for the
# same entry. Nothing is translated at runtime: the browser only ever fetches
# finished HTML shipped with the site, so no model download is ever triggered.
LANGS = {"hi": "हिंदी"}


def load_entry(path, lang="en"):
    """Parse one authored page (an English source or a translation of one)."""
    md = path.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(.*)$", md, re.M)
    summary = field(md, f"Summary-{lang}") if lang != "en" else field(md, "Summary")
    return {
        "lang": lang,
        "title": title.group(1).strip() if title else path.stem,
        "summary": strip_vendor_tags(summary or field(md, "Summary") or field(md, "What it is")),
        "date": field(md, "Logged", DEFAULT_DATE),
        "url": field(md, "Site"),
        "html": convert(body_of(md)),
    }


def load_entry_set(slug):
    """Load an entry plus every available translation of it."""
    pages = {"en": load_entry(SRC / f"{slug}.md", "en")}
    for lang in LANGS:
        alt = SRC / f"{slug}.{lang}.md"
        if alt.exists():
            pages[lang] = load_entry(alt, lang)
    return pages


def lang_toggle(slug, current, pages):
    """Inline language links; the current language is plain text, not a link."""
    links = []
    for code, label in [("en", "English")] + list(LANGS.items()):
        if code not in pages:
            continue
        name = f"{slug}.html" if code == "en" else f"{slug}.{code}.html"
        if code == current:
            links.append(f"<strong>{label}</strong>")
        else:
            links.append(f'<a href="{name}">{label}</a>')
    return f'<p class="langs">{" · ".join(links)}</p>' if len(links) > 1 else ""


def shell(title, body, back=True, lang="en"):
    nav = (
        f'<p class="back"><a href="{SITE}/">← All learnings</a> &nbsp;·&nbsp; '
        f'<a href="{REPO}">Source on GitHub</a></p>'
        if back
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="Daily learnings and tools explored.">
<script>{THEME_INIT}</script>
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" id="theme-toggle" type="button" aria-live="polite"></button>
<div class="wrap">
{nav}
{body}
<footer class="site">
  <p><a href="{REPO}">GitHub</a> · <a href="{REPO}/blob/main/README.md">README</a> · built from markdown, no framework.</p>
</footer>
</div>
<script>{THEME_JS}</script>
</body>
</html>
"""


def main():
    sets = {}
    for path in sorted(SRC.glob("*.md")):
        if path.name.endswith(tuple(f".{lang}.md" for lang in LANGS)):
            continue  # a translation, loaded with its English source below
        sets[path.stem] = load_entry_set(path.stem)

    (OUT / "tools").mkdir(parents=True, exist_ok=True)

    written = 0
    for slug, pages in sets.items():
        for code, entry in pages.items():
            name = f"{slug}.html" if code == "en" else f"{slug}.{code}.html"
            head = (
                f'<div class="page-head"><h1>{inline(entry["title"])}</h1>'
                f'<p class="m">{html.escape(entry["date"])}'
                + (f' &nbsp;·&nbsp; <a href="{html.escape(entry["url"])}">{"साइट देखें" if code != "en" else "visit site"}</a>' if entry["url"] else "")
                + "</p>"
                + lang_toggle(slug, code, pages)
                + "</div>"
            )
            page = shell(
                entry["title"], head + f'<div class="entry">{entry["html"]}</div>', lang=code
            )
            (OUT / "tools" / name).write_text(page, encoding="utf-8")
            written += 1

    cards = "\n".join(
        f'<a class="card" href="tools/{slug}.html">'
        f'<div class="t">{inline(pages["en"]["title"])}</div>'
        f'<div class="d">{inline(pages["en"]["summary"])}</div>'
        f'<div class="m">{html.escape(pages["en"]["date"])}'
        + ("　·　हिंदी" if len(pages) > 1 else "")
        + "</div></a>"
        for slug, pages in sorted(
            sets.items(), key=lambda kv: kv[1]["en"]["date"], reverse=True
        )
    ) or '<p class="empty">No entries yet.</p>'

    body = f"""<header class="site">
<h1>Daily Learnings</h1>
<p>New things learned from daily routine, and new tools explored. One page per entry.</p>
<nav>
<a href="{REPO}">GitHub</a>
<a href="{REPO}/blob/main/README.md">README</a>
<a href="https://raw.githubusercontent.com/pavnxet/daily-learnings/main/README.md">Raw</a>
</nav>
</header>
<h2>Entries</h2>
{cards}"""

    (OUT / "index.html").write_text(
        shell("Daily Learnings", body, back=False), encoding="utf-8"
    )
    translated = sum(1 for pages in sets.values() for code in pages if code != "en")
    print(f"built {len(sets)} entr{'y' if len(sets) == 1 else 'ies'} "
          f"({written} page(s), {translated} translation(s)) + docs/index.html")


if __name__ == "__main__":
    main()
