# Learning — daily-learnings

Domain knowledge and conventions for this repo. Edit in place; no duplicates.

## Repo shape

- `tools/<slug>.md` — one page per explored tool. **Source of truth.**
- `docs/` — generated site served by GitHub Pages. **Never hand-edit.**
- `generate.py` — builds `docs/` from `tools/`. Run after any entry change.
- `README.md` — human summary and hand-maintained index table.
- `learning/` — agent memory (this folder). Not part of the published content.

## GitHub Pages gotchas

- **Pages serves `.md` as plain text**, not rendered HTML. Linking the site at raw markdown shows the source. That is why entries are converted to styled HTML. (The `.md` files still render properly on github.com.)
- **Site must be published from `docs/` on `main`** — configured via `POST /repos/{owner}/{repo}/pages` with `{"source":{"branch":"main","path":"/docs"}}`. `gh repo create` does not enable Pages.
- **`docs/.nojekyll` disables Jekyll.** Without it Pages runs the files through Jekyll, which is unnecessary for plain HTML.
- **Relative link depth matters.** `docs/index.html` sits at the site root but entry pages live in `docs/tools/`, so index cards must link to `tools/<slug>.html`, not `<slug>.html`. The back-link on an entry page correctly uses the bare site root.
- First build takes roughly 1–2 minutes; `gh api repos/{owner}/{repo}/pages` reports `building` then `built`. An `HTTP 200` alone is not proof of success — GitHub can serve a 200 "not found" page. Check for an expected element such as `<h1>` in the body.

## Writing rules discovered so far

- **Vendor pages are marketing, not documentation.** The SmailPro `/api` page states no endpoints and no code samples — it links out to a separate docs hub (`sonjj.com/docs`) on a **different domain**. Treat any figure on a vendor's own landing page (pool size, acceptance rate, delivery speed) as a claim until an independent source or a live test confirms it.
- **Tag claims inline at the number, never a blanket section note.** A section-level disclaimer got skipped by the generator AND failed the repo's own honesty rule. Each figure carries its own `(vendor claim — unverified)`.
- **Note the account model, not just the address.** A "temporary Gmail" is not a fresh Gmail — it is a credential for a mailbox the vendor also controls. That distinction decides whether a use case is safe, and it belongs in the entry.
- **Disposable-domain blocklists are the reason mainstream temp-mail fails.** When a signup form silently never sends the verification mail, the cause is usually a domain blocklist, not a broken form. Worth checking before debugging the wrong thing.
- **CAPTCHA-protected temp-mail flows need an out-of-band solver.** Bypassing Cloudflare Turnstile from a script means running a separate solver service (e.g. Boterdrop-Solver) — not a pure-Python dependency.

## Tooling notes

- Verified working on Windows with `python` on PATH. The generator is stdlib-only (`html`, `re`, `pathlib`) — no install step.
- Write files as UTF-8. Entries use em dashes and en dashes; reading or writing them as anything else produces mojibake in the published HTML.
- **Shell-quoting trap (Windows/PowerShell)**: `python -c "...re.search(r'<div class=\"entry\">...')..."` fails because PowerShell mangles nested quotes — it produced a `SyntaxError: unterminated string literal`, not a Python problem. Write a throwaway `.py` verifier file and run it instead of fighting inline quoting. Delete it afterwards.
- **Theme persistence must be applied before the stylesheet.** Rendering the saved theme in a script at the end of `<body>` causes a flash of the system theme first. `THEME_INIT` is inlined in `<head>` ahead of `<style>` for exactly this reason. `THEME_JS` (interaction + label) is a separate script at the end of `<body>`, where the button exists.
- **CSS custom-property overrides rely on source order, not specificity.** `:root` and `[data-theme=light]` have equal specificity (0,1,0), so the theme blocks must appear *after* the `prefers-color-scheme` media query to win. Moving them earlier silently breaks the toggle.
- **Validate unknown JS with `node --check`** on the generated output rather than counting braces — balanced-brace checks pass on plenty of broken syntax.
