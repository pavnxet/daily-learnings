# Learning — daily-learnings

Domain knowledge and conventions for this repo. Edit in place; no duplicates.

## Repo shape

- `tools/<slug>.md` — one page per explored tool.
- `README.md` — index table; one row per entry.
- `learning/` — agent memory (this folder). Never part of the published content.

## Writing rules discovered so far

- **Vendor pages are marketing, not documentation.** The SmailPro `/api` page states no endpoints and no code samples — it links out to a separate docs hub (`sonjj.com/docs`) on a **different domain**. Treat any figure on a vendor's own landing page (pool size, acceptance rate, delivery speed) as a claim until an independent source or a live test confirms it.
- **Note the account model, not just the address.** A "temporary Gmail" is not a fresh Gmail — it is a credential for a mailbox the vendor also controls. That distinction decides whether a use case is safe, and it belongs in the entry.
- **Disposable-domain blocklists are the reason mainstream temp-mail fails.** When a signup form silently never sends the verification mail, the cause is usually a domain blocklist, not a broken form. Worth checking before debugging the wrong thing.
- **CAPTCHA-protected temp-mail flows need an out-of-band solver.** Bypassing Cloudflare Turnstile from a script means running a separate solver service (e.g. Boterdrop-Solver) — not a pure-Python dependency.
