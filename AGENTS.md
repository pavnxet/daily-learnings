# daily-learnings Subproject Agent Instructions

> **Master Protocol**: Read the master governance rules at [file:///e:/Codes/Testing/AGENTS.md](file:///e:/Codes/Testing/AGENTS.md).
> **Local Memory & Learning**: All memory, session history, ADRs, and execution maps for this project are stored strictly inside [./learning/](./learning/).
> **`learning/` IS GITIGNORED — LOCAL ONLY.** It is tracking-excluded, so it never appears on GitHub, in the Pages build, or in a fresh clone. It exists only on the machine it was written on. Keep writing to it; never expect it from a clone, and never link to it from published content (`README.md`, `tools/`, `docs/`).
> - **Domain Knowledge & Fixes**: [./learning/learning.md](./learning/learning.md)
> - **Architecture Decisions (ADRs)**: [./learning/DECISIONS.md](./learning/DECISIONS.md)
> - **Execution Flow & Call Graph**: [./learning/EXECUTION_FLOW.md](./learning/EXECUTION_FLOW.md)
> - **Session History Log**: [./learning/summary.md](./learning/summary.md)

## What this repo is

A daily log of new learnings from routine work and new tools explored. Not a wiki, not a tutorial dump — one file per tool or topic, written the day it was learned.

## Conventions

- **One tool = one file** in [`tools/`](./tools/), named `<tool-slug>.md` (lowercase, hyphens).
- **File skeleton**: What it is → Why it matters → How to use (free path first, API for automation) → Limits & risks → Verdict.
- **Always link the source URL** so the claim can be re-checked later.
- **Separate vendor claims from verified facts.** Mark anything taken from a vendor's own marketing as `(vendor claim — unverified)`. Do not restate it as fact.
- **New entry ⇒ add one line to the README table** and log it in [./learning/summary.md](./learning/summary.md).
- Categories beyond `tools/` get their own top-level folder and one README row per entry.
- **After any change to `tools/` or `README.md`, run `python generate.py`** to rebuild `docs/`. Never hand-edit anything in `docs/` — it is generated output.

---

## New-learning submission protocol (MANDATORY)

When the user sends a tool, website, service, product, or anything new they learned — even as a bare URL with no explanation — perform the following. Do not ask the user to do research or to fill in details; research it yourself.

### 1. Research deeply across independent sources

The user's instruction is **deep multi-source research**. Consult all of these that exist for the subject:

| Source type | Why |
|---|---|
| The vendor's own site, pricing, and docs | Establishes what it claims to do |
| Official API/developer reference | The real capabilities and limits — often a different domain from the marketing site |
| Package registry (PyPI/npm), GitHub repo, issues | Third-party wrappers, maintenance state, known bugs |
| Independent reviews, comparisons, forum threads | Criticism the vendor will never publish |
| The tool's terms of service / acceptable-use policy | Whether a use case is even permitted |

Use `web_search` to find candidates and `web_fetch` to read the actual pages — do not write an entry from search snippets alone.

### 2. Separate claims from facts

- Tag every figure sourced from the vendor's own marketing as `(vendor claim — unverified)`, **inline where the number appears**. A blanket note at the top of a section is not enough.
- Write the literal string `vendor claim` inside the parentheses — that exact phrase is what the generator highlights in the site output.
- Never restate a vendor performance number, user count, pool size, delivery time, or acceptance rate as the project's own finding.
- If a claim can't be verified, say so plainly in **Limits & risks** rather than dropping it.

### 3. Write the entry

- Create `tools/<slug>.md` — lowercase, hyphens.
- Keep the metadata block at the top in this exact order, since the site generator reads it:

  ```markdown
  # <Title>

  - **Site**: <url>
  - **Logged**: <YYYY-MM-DD>
  - **Summary**: <one sentence — this becomes the card text on the site index>
  - **Category**: <short category>
  ```

- Sections, in order: `## What it is`, `## Why it matters`, `## How to use`, `## Limits & risks`, `## Verdict`, `## Sources`.
- `## How to use` leads with the free/manual path, then automation, with copy-pasteable code.
- `## Limits & risks` is mandatory and must cover: what it cannot do, what is unverified, any privacy/security concern, and any terms-of-service risk. Flag clearly when use is limited to permitted cases such as testing your own systems.
- `## Sources` lists every URL consulted as `- [label](url) — url`.
- **Write the mechanism, not the pitch.** The most valuable line in an entry explains *why* the thing works (e.g. "real provider domains clear domain blocklists" beats "great for privacy").

### 4. Close the loop

1. Create the file in `tools/`, add its `Summary` line.
2. Add a numbered row to the **Index** table in `README.md`, and add the entry to the `What's in here`/index lists if the count changes.
3. Write the Hindi translation as `tools/<slug>.hi.md` (see below).
4. Run `python generate.py` and confirm it reports the expected number of pages **and translations**.
5. Append a dated entry to [./learning/summary.md](./learning/summary.md).
6. Fold any generalizable insight (a pattern that applies beyond this one tool) into [./learning/learning.md](./learning/learning.md).

---

## Translation protocol (MANDATORY)

Every entry ships in **English and Hindi**. This is done at *build* time by the agent, never at runtime — no visitor ever downloads a model, and there is no translation API. Static pre-built HTML is the whole point, so do not add client-side translation.

### Creating a translation

- Author it as `tools/<slug>.hi.md`, a sibling of `tools/<slug>.md`.
- **Same structure, same order.** Only the prose is translated. Keep the `#` title, all `##` sections in the same sequence, the same tables (same rows/columns), the same `Site` / `Logged` / `Category` metadata values, and the same code blocks. The generator pairs the two pages; a structural mismatch shows up as a broken-looking toggle page.
- **Never translate technical substance.** Leave in English: code blocks and commands, model IDs and endpoint paths, URLs and filenames, product names (Gmail, Outlook, FastAPI, OpenAI), and the literal string `vendor claim`. Translating `` `lc_router.py` `` or `POST /v1/chat/completions` makes the entry wrong, not bilingual.
- **Keep inline markup intact** — `**bold**`, links, backticks, and the `(vendor claim — unverified)` tag must survive verbatim, in the same positions.
- **Translate meaning, not words.** Use natural Hindi technical register: loanwords in Devanagari where that is how Indian technical writing actually reads (डोमेन, ब्लॉकलिस्ट, वेरिफ़िकेशन, क्रेडेंशियल), native Hindi where it reads better (सीमाएँ और जोखिम, निष्कर्ष, स्रोत).
- **Section headings are standardised**: यह क्या है / यह क्यों मायने रखता है / इस्तेमाल कैसे करें / सीमाएँ और जोखिम / निष्कर्ष / स्रोत.
- **No runtime translation libraries. Ever.** Adding `@huggingface/transformers` or any in-browser translator contradicts the requirement that visitors download nothing.
- **Say so when you cannot verify a translation.** Never claim a Hindi page was proofread if it was not.

### Adding another language later

Add the code and its label to `LANGS` in `generate.py` (e.g. `{"hi": "हिंदी", "mr": "मराठी"}`) and supply `tools/<slug>.<code>.md` for the entries you want translated. The toggle, the `<html lang>` attribute and the index markers are generated automatically; entries without that file are simply left in English with no toggle.

