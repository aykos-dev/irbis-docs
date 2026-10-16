---
description: Build one feature across api/web/app — spec, approval gate, implement, review, wrap up
argument-hint: <slug> — <behaviour, constraints, out of scope>
---
Build feature: $ARGUMENTS

Read STATUS.md, PROJECT.md, and only the relevant files in decisions/ first.

PHASE 1 — SPEC (then STOP)
Write features/<slug>.md from features/_TEMPLATE.md: goal, surfaces touched (api/web/app),
endpoints, data model changes, acceptance criteria (incl. loading/empty/error/offline),
out of scope. List your assumptions and open questions.
STOP and wait for my approval. Do not write code. Do not start phase 2 until I reply "approved".

PHASE 2 — API (subagent: api-dev) — skip if api not touched
Pass it: the spec path and the slug. It creates branch feat/<slug>, writes failing tests from
the acceptance criteria first, implements, runs `npm run check` until green, runs
`npm run openapi:export`, commits. It returns a ≤15-line summary + final check output.

PHASE 3 — CLIENTS (subagents: web-dev, app-dev — only for touched surfaces, in parallel)
Each: branch feat/<slug>, `npm run gen:api`, implement using generated hooks only,
`npm run check` until green, commit. Each returns a ≤15-line summary + final check output.

PHASE 4 — REVIEW (subagent: reviewer)
Review all diffs (`git diff main...feat/<slug>` in each touched repo) against the spec and the
slop checklist in CLAUDE.md. Send blocking issues back to the owning dev agent, then re-review.
Max 2 fix rounds; if still blocked, stop and report to me.

PHASE 5 — WRAP UP
Mark the spec Done. Update STATUS.md (Done line with short commit hashes per repo; Next).
Commit in irbis-docs. Do not push anything.
Reply with: what changed per repo, final `npm run check` output per repo, anything skipped or
deferred, and a reminder to `/clear` before the next feature.
