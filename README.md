# Daily Learnings

**[→ Read the site](https://pavnxet.github.io/daily-learnings/)** · [GitHub Pages](https://pavnxet.github.io/daily-learnings/)

New things learned from daily routine, and new tools explored. One page per entry — what it is, why it's worth knowing, how to actually use it, and what it can't do.

---

## What's in here

| Area | Contents |
|---|---|
| **[tools/](tools/)** | One page per tool, service, or website explored. The main body of this repo. |
| **[docs/](docs/)** | The generated website served by GitHub Pages. Built from `tools/`, never edited by hand. |
| **[README.md](README.md)** | This index. |
| **[AGENTS.md](AGENTS.md)** | The logging protocol — how a new learning gets researched and written up. |
| **[learning/](learning/)** | Research notes: conventions, decisions, session history. Local only — gitignored, not part of the site or the repo. |

## Index

| # | Entry | What it is | Logged |
|---|---|---|---|
| 1 | [SmailPro — temporary Gmail & Outlook inboxes](tools/smailpro.md) | Disposable inboxes on **real Gmail and Outlook addresses**, which clears the domain blocklists that silently kill ordinary temp-mail verification | 2026-10-10 |
| 2 | [lucky-cat-api + radio-house-api](tools/ai-api-bridge.md) | Two local FastAPI bridges wrapping free AI chat sites (Proton Lumo, TryingOpen) into one OpenAI-compatible endpoint — ~24 models from a `baseURL` swap | 2026-10-10 |
| 3 | [Intelligence X (intelx.io)](tools/intelx.md) | Freemium OSINT search engine over 200 billion+ records — breaches, stealer logs, pastes, darknet, historical web — searched by **selector**, not keyword | 2026-10-10 |
| 4 | [WhatsMyName](tools/whatsmyname.md) | Community-maintained JSON dataset of 700+ sites answering "does this username exist?" — the data layer behind most username checkers | 2026-10-10 |
| 5 | [ProxyNova anonymous email](tools/proxynova-anonymous-email.md) | No-signup web form that mails anyone from a rotating sender pool, so the recipient cannot trace it to you — capped at 5 emails/day | 2026-10-10 |
| 6 | [Face Detection & Comparison demo](tools/face-comparison-demo.md) | Browser demo comparing two uploaded faces — a teaching example of the detect → align → embed → compare pipeline | 2026-10-10 |

*Each entry page carries a `Summary` line; the website index is built from those lines. Entries marked **हिंदी** on the site also have a Hindi translation.*

## Languages

Every entry is available in **English and Hindi**, switchable from the language links at the top of each entry page. Hindi is served as finished static HTML — `docs/tools/<slug>.hi.html` — so **nothing is translated in the browser and no model is ever downloaded by a visitor.** The pages are pre-built, load instantly, work offline, and cost nothing to serve.

- English source: `tools/<slug>.md`
- Hindi translation: `tools/<slug>.hi.md` (optional — an entry without one simply shows no language toggle)

Technical substance stays in English inside both versions: code blocks, commands, model IDs, URLs, filenames, and product names. Translating `` `lc_router.py` `` or `POST /v1/chat/completions` would be actively harmful, so those are left alone and the surrounding prose is translated.

**Why pre-built rather than a live translator:** accurate machine translation needs either a large server or a large model. GitHub Pages can host neither, and in-browser models mean a ~100 MB+ download on first visit. Translating at build time is the only approach that gives good quality with **zero download and no API**, which is why it's used here.

## How an entry is written

Every entry follows the same five sections, so entries stay comparable and skimmable:

1. **What it is** — one paragraph, plain language.
2. **Why it matters** — the actual mechanism or problem it solves, not the marketing pitch.
3. **How to use** — the free path first, the API/automation path second, with working code.
4. **Limits & risks** — what it cannot do, what is unverified, what is unsafe or against terms of service.
5. **Verdict** — who should use it, and for which specific job.

Rules that keep the log honest:

- **Vendor marketing is tagged, not repeated.** Any figure taken from a company's own page is marked `(vendor claim — unverified)` until independently confirmed. Performance numbers, pool sizes, and acceptance rates are claims, not facts.
- **The source URL is always linked**, so any claim can be re-checked later.
- **Limits are mandatory.** An entry with no risks section is an advertisement, not a learning.

## Submitting a new learning

Send the link, name, or rough description of the tool — one line is enough. Each submission is then researched across multiple independent sources (vendor site, official docs, package registry, third-party reviews and known criticisms), written up as `tools/<slug>.md`, **translated to `tools/<slug>.hi.md`**, added to the index, and rebuilt into the site. No further input is needed.

## The site

`docs/` is generated from `tools/` — GitHub Pages serves Markdown as plain text, so each entry gets a styled HTML page instead:

```bash
python generate.py     # rebuild docs/ after adding or editing an entry or translation
```

Minimal theme, no framework, no dependencies, works in light and dark mode, bilingual. Pages is published from **`main` / `docs`**.

### Theme

The site follows your operating system's light/dark setting by default. A small toggle sits in the top-right corner of every page; clicking it switches theme and remembers the choice in `localStorage` across pages and visits. Clear the site's saved data (or use a private window) to fall back to following the system again.

The saved theme is applied by a short inline script placed **before** the stylesheet, so a page never flashes the wrong colours before settling.

## Structure

```
daily-learnings/
├── README.md                  this index
├── AGENTS.md                  logging protocol for AI agents
├── generate.py                builds docs/ from tools/
├── tools/                     ← source of truth
│   ├── smailpro.md            one English entry
│   └── smailpro.hi.md         its Hindi translation
├── docs/                      generated site (GitHub Pages)
│   ├── index.html
│   └── tools/
│       ├── smailpro.html
│       └── smailpro.hi.html
└── learning/                  research notes, not published (gitignored)
```

To add a language, add its code and label to `LANGS` in `generate.py` and supply `tools/<slug>.<code>.md` files — the toggle, `lang` attribute and index markers follow automatically.

---

<sub>Plain Markdown in, a small static site out. No Jekyll, no theme, no build dependencies.</sub>
