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
| **[learning/](learning/)** | Research notes: conventions, decisions, session history. Not part of the site. |

## Index

| # | Entry | What it is | Logged |
|---|---|---|---|
| 1 | [SmailPro — temporary Gmail & Outlook inboxes](tools/smailpro.md) | Disposable inboxes on **real Gmail and Outlook addresses**, which clears the domain blocklists that silently kill ordinary temp-mail verification | 2026-10-10 |

*Each entry page carries a `Summary` line; the website index is built from those lines.*

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

Send the link, name, or rough description of the tool — one line is enough. Each submission is then researched across multiple independent sources (vendor site, official docs, package registry, third-party reviews and known criticisms), written up as `tools/<slug>.md`, added to the index, and rebuilt into the site. No further input is needed.

## The site

`docs/` is generated from `tools/*.md` — GitHub Pages serves Markdown as plain text, so each entry gets a styled HTML page instead:

```bash
python generate.py     # rebuild docs/ after adding or editing an entry
```

Minimal theme, no framework, no dependencies, works in light and dark mode. Pages is published from **`main` / `docs`**.

## Structure

```
daily-learnings/
├── README.md            this index
├── AGENTS.md            logging protocol for AI agents
├── generate.py          builds docs/ from tools/*.md
├── tools/               one markdown page per entry  ← the source of truth
│   └── smailpro.md
├── docs/                generated site (GitHub Pages)
│   ├── index.html
│   └── tools/smailpro.html
└── learning/            research notes, not published
```

---

<sub>Plain Markdown in, a small static site out. No Jekyll, no theme, no build dependencies.</sub>
