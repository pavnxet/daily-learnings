# Session Summary — daily-learnings

Append-only. Newest entries at the end. Never delete or overwrite past entries.

---

## 2026-10-10 — Repo created + first entry (SmailPro)

**Task**: Create a repo for storing new learnings from daily routine and newly explored tools. First subject: https://smailpro.com/temporary-email

**Actions taken**:
- Researched SmailPro via web search and direct fetches of the vendor's temporary-email tool page, the vendor API overview page, the PyPI page for the unofficial `smailpro-api` Python wrapper, and its GitHub repo.
- Created `daily-learnings/` with the protocol-mandated scaffolding **first**: `AGENTS.md`, `learning/learning.md`, `learning/DECISIONS.md`, `learning/EXECUTION_FLOW.md`, `learning/summary.md`.
- Created `README.md` — index table plus the add-an-entry procedure.
- Created `tools/smailpro.md` — full entry: what it is, why it matters (domain-blocklist failure mode), browser free path, API automation path, Python wrapper with its solver caveat, limits & risks, verdict, sources.

**Files created**:
- `daily-learnings/AGENTS.md`
- `daily-learnings/README.md`
- `daily-learnings/learning/learning.md`
- `daily-learnings/learning/DECISIONS.md`
- `daily-learnings/learning/EXECUTION_FLOW.md`
- `daily-learnings/learning/summary.md`
- `daily-learnings/tools/smailpro.md`

**Results**: Repo is live and has one entry. No build step, no dependencies, no git init (not requested).

**Notes for the next session**:
- Vendor figures in `tools/smailpro.md` are tagged `(vendor claim — unverified)`. No live test was run — the free flow was never exercised and no API key exists. **If you get an API key, test acceptance on one real target form and upgrade those tags to verified facts with a dated note.**
- System date is 2026-10-10; an initial draft of the ADRs used a wrong date and was corrected in place before finishing.
- Nothing outside `daily-learnings/` was created or modified.

---

## 2026-10-10 (session 2) — Published to GitHub + Pages website

**Task**: Create a public GitHub repo, put this log in it, present a summary in the README, add an `index.html` on GitHub Pages acting as a minimal blog-style site for all future learnings, and add a rule to `AGENTS.md` covering future submissions ("I send a new tool, you research it deeply and add it").

**Actions taken**:
- Confirmed GitHub auth: `gh` 2.87.3, account `pavnxet`, scopes `gist, read:org, repo, workflow`.
- Wrote `generate.py` — a dependency-free (stdlib `html`/`re`/`pathlib`) generator that converts `tools/*.md` into `docs/tools/<slug>.html` and rebuilds `docs/index.html` from entry metadata.
  - Needed because **GitHub Pages serves `.md` as plain text**, so pointing the site at the markdown would show raw source.
- Wrote the minimal site theme inline in the generator: system font stack, 46rem measure, CSS variables, `prefers-color-scheme` light/dark, card index, tables/code styling.
- Added `docs/.nojekyll` to switch off Jekyll.
- Rewrote `README.md` as the repo summary: what's in here, an indexed table of entries, the five-section entry format, the honesty rules, how to submit a new learning, and the site build command.
- Added a **New-learning submission protocol** to `AGENTS.md`: deep multi-source research (vendor site, official docs, registry/repo, independent reviews, ToS), inline `(vendor claim — unverified)` tagging, exact metadata block contract, mandatory Limits & risks coverage, then the close-the-loop checklist.
- Created public repo `pavnxet/daily-learnings`, pushed `main`, enabled Pages from `main`/`docs` via `POST /repos/pavnxet/daily-learnings/pages`, confirmed `status=built`, and verified both the index and entry page return HTTP 200 with real content.
- Updated `learning/` memory: `learning.md` (Pages gotchas, repo shape, tooling notes), `DECISIONS.md` (ADR-002 marked superseded; new ADR-004/005/006), `EXECUTION_FLOW.md` (build graph, write path), this log.

**Files created/modified**:
- Created: `generate.py`, `docs/index.html`, `docs/tools/smailpro.html`, `docs/.nojekyll`
- Modified: `README.md` (rewritten), `AGENTS.md`, `tools/smailpro.md` (metadata + inline vendor tags), `learning/learning.md`, `learning/DECISIONS.md`, `learning/EXECUTION_FLOW.md`, `learning/summary.md`
- Removed: `build.py`, `_check.py` (both scratch files created and discarded during the session)

**Bugs found and fixed during this session** (all caught by verification, none reached the remote before being fixed):
1. Index cards linked to `smailpro.html`, but entry pages are written to `docs/tools/` — the card 404'd. Fixed to `tools/<slug>.html`.
2. `##` headings were rendered as `<h3>` (an off-by-one level bump). Fixed; added `.entry>h2:first-child` styling so the entry's first section heading does not look like an index label.
3. The vendor-claim highlighter matched the literal string `vendor claim`, but the entry said `vendor claims` (plural) in a single blanket section note — so **nothing was tagged** and the repo's own honesty rule was silently unmet. Fixed by tagging each figure inline; the matcher stays singular on purpose, so the plural phrase can no longer pass unnoticed.

**Results**: Repo is public and live — https://github.com/pavnxet/daily-learnings — with the site at https://pavnxet.github.io/daily-learnings/ (HTTPS enforced, `status=built`, both pages verified 200).

**Notes for the next session**:
- Pages redeploys automatically on push to `main`. After adding an entry, always run `python generate.py` **before** committing, or the site shows a stale index with a missing page.
- `docs/` is generated output — never hand-edit it.
- SmailPro performance figures remain unverified vendor claims. Still no live test and no API key.

---

## 2026-10-10 (session 3) — Light/dark theme toggle

**Task**: Add a theme toggle option to the webpage.

**Actions taken**:
- Added two scripts and a button to the shared page shell in `generate.py`, so the toggle appears on every page (index and all entry pages) automatically:
  - `THEME_INIT` — inlined in `<head>` **before** `<style>`; applies a `localStorage`-saved theme to `document.documentElement.dataset.theme`. Placed ahead of the stylesheet so a saved dark theme never flashes light first.
  - `THEME_JS` — at the end of `<body>` (where the button exists); flips the theme on click, persists it, and keeps the icon and `aria-label` in sync with the effective theme.
  - `<button class="theme-toggle">` — fixed top-right, outlined pill, hidden in print via `@media print`.
- Restructured the CSS: `--mark` was dead after the `<strong>` switch, so it was dropped; added explicit `[data-theme=light]` / `[data-theme=dark]` variable blocks **after** the `prefers-color-scheme` query, since both selectors have equal specificity and source order is what makes the explicit choice win.
- Documented the behaviour under a new **Theme** section in `README.md` (system default, click to override, remembered, clear data to return to auto).

**Files modified**:
- `generate.py` (CSS, `THEME_INIT`, `THEME_JS`, `shell()`)
- `README.md`
- `learning/learning.md`, `learning/EXECUTION_FLOW.md`, `learning/summary.md`
- Regenerated: `docs/index.html`, `docs/tools/smailpro.html`
- Created and removed: `_verify.py`, `_theme.js` (scratch)

**Verification**:
- Both generated pages contain the button, 2 script tags, and the 2 `[data-theme=]` rule sets.
- Head order confirmed as `script, style, /head` — init before styles.
- Extracted the generated JS and ran `node --check` (exit 0, Node v24.19.0). Brace counting was also clean, but `node --check` is the real signal.
- Escapes verified to survive generation as `\u2600` / `\u263D` (written `\\uXXXX` in the Python source, since f-strings — unlike the JS — do not process inner escapes).

**Notes for the next session**:
- Not verified in a real browser: the visual result, the actual no-flash behaviour on reload, and cross-page persistence are confirmed at the HTML/JS level only. If any doubt, open the Pages URL and toggle it.
- The toggle is deliberately two-state. The system preference is only followed until the first click; there is no on-page control to return to auto (clearing site data does it). Adding a third "auto" state was skipped as unnecessary.
- `theme-toggle` uses `position:fixed`, which is fine at the ~46rem content width but would overlap content on a very narrow viewport.


