# Execution Flow — daily-learnings

## Entry points

| Path | Role |
|---|---|
| https://pavnxet.github.io/daily-learnings/ | The published site (GitHub Pages, `main` / `docs`). |
| `README.md` | Human entry point on GitHub. Summary + hand-maintained index table. |
| `tools/<slug>.md` | One tool entry. **The actual content and source of truth.** |
| `AGENTS.md` | Agent entry point. Conventions + the new-learning submission protocol. |
| `generate.py` | The build. Converts entries to `docs/`. |

## Build / call graph

`tools/*.md` → `generate.py` → `docs/tools/<slug>.html` + `docs/index.html` → GitHub Pages

Steps inside `generate.py::main`:

1. Glob `tools/*.md` (sorted), parse each with `build_entry`.
   - Title from the first `# ` line; `Summary` and `Logged` from the metadata bullets.
   - `body_of` drops the title and metadata, then linkifies bare URLs in Sources.
   - `convert` renders the markdown subset; `inline` escapes HTML then applies inline styles.
2. Write one page per entry via `shell(...)`, wrapped in `<div class="entry">`.
3. Build `docs/index.html` from the collected `Summary`/`Logged` metadata, newest first.

Run: `python generate.py` → prints `built N entry page(s) + docs/index.html`.

### Page shell (`shell()`)

Every generated page shares one shell, so any change there lands on all pages at once:

- `<script>{THEME_INIT}</script>` — in `<head>`, **before** `<style>`, applies the saved theme with no flash.
- `<style>{CSS}</style>` — theme variables, then `[data-theme=light|dark]` overrides *after* the system-preference query.
- `<button class="theme-toggle">` — fixed top-right, present on every page.
- `<script>{THEME_JS}</script>` — at the end of `<body>`; toggles the theme, persists it to `localStorage`, and keeps the icon/`aria-label` in sync.

Theme state lives in `document.documentElement.dataset.theme` and is absent when following the system.

## Write path for a new entry

1. Research the tool deeply — see the submission protocol in `AGENTS.md` (vendor site, official docs, registry/repo, independent reviews, ToS).
2. Create `tools/<slug>.md` using the skeleton in `AGENTS.md`, tagging vendor claims inline.
3. Add a numbered row to the Index table in `README.md`.
4. Run `python generate.py`; confirm the entry count and spot-check the output HTML.
5. Append a dated entry to `learning/summary.md`; fold generalizable facts into `learning/learning.md`.
6. Commit and push — Pages redeploys automatically from `main`/`docs`.

## Recent Changes

| Date | Change |
|---|---|
| 2026-10-10 | Repo created. `README.md`, `AGENTS.md`, `learning/` (4 files), `tools/smailpro.md`. |
| 2026-10-10 | Added `generate.py` + `docs/` site for GitHub Pages; rewrote `README.md` as the repo summary. Public repo `pavnxet/daily-learnings` created, Pages enabled from `main`/`docs` (HTTPS), verified live. Added the new-learning submission protocol to `AGENTS.md`. |
| 2026-10-10 | Fixed generator: `##`→`<h2>` (was `<h3>`), index card href `tools/<slug>.html` (was root-relative and broken), vendor tags now `<strong>` and applied inline in the entry. |
| 2026-10-10 | Added light/dark theme toggle to every page (`THEME_INIT` in head before CSS to avoid a flash, `THEME_JS` at end of body, `localStorage` persistence, system default when unset). Documented under "Theme" in `README.md`. JS validated with `node --check`. |
