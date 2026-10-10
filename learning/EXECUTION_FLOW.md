# Execution Flow — daily-learnings

## Entry points

| Path | Role |
|---|---|
| `README.md` | Human entry point. Index table of every logged learning. |
| `tools/<slug>.md` | One tool entry. The actual content. |
| `AGENTS.md` | Agent entry point. Conventions for adding entries. |

This repo has no runtime, no build, and no call graph. "Flow" here is the write path for a new entry.

## Write path for a new entry

1. Research the tool (vendor site, docs, third-party reviews, package registry).
2. Create `tools/<slug>.md` using the skeleton in `AGENTS.md`.
3. Append one row to the table in `README.md`.
4. Append a dated entry to `learning/summary.md`; fold new generalizable facts into `learning/learning.md`.

## Recent Changes

| Date | Change |
|---|---|
| 2026-10-10 | Repo created. `README.md`, `AGENTS.md`, `learning/` (4 files), `tools/smailpro.md`. |
