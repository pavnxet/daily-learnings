# Architecture Decision Records — daily-learnings

## ADR-001: One file per tool instead of one growing README

- **Date**: 2026-10-10
- **Status**: Accepted
- **Context**: Daily entries accumulate. A single README would grow into an unnavigable document and make every new entry a merge conflict.
- **Decision**: One markdown file per tool in `tools/<slug>.md`, with a one-row index in `README.md`.
- **Consequences**: Adding a tool touches two files (entry + index row). In return, entries stay independently readable and diffable, and a broken entry cannot corrupt the rest of the log.

## ADR-002: No site generator, no build step

- **Date**: 2026-10-10
- **Status**: Accepted
- **Context**: The repo is read on GitHub and by agents as plain text.
- **Decision**: Plain markdown only. No Jekyll/Hugo/Astro, no CI, no dependencies.
- **Consequences**: Nothing to maintain or debug; zero tooling cost. Cost: no search, tags, or themes — acceptable until the log is large enough to need an index, which the README table already provides.

## ADR-003: Mark unverified vendor claims inline

- **Date**: 2026-10-10
- **Status**: Accepted
- **Context**: Tool research relies heavily on vendor marketing pages. Pasted-at-face-value marketing ages into misinformation, and a future reader cannot tell which lines were tested.
- **Decision**: Tag vendor-sourced figures `(vendor claim — unverified)` in the entry text, and keep a separate "Limits & risks" section.
- **Consequences**: Entries read slightly less cleanly, but every number carries its provenance and can be re-verified or deleted with confidence.
