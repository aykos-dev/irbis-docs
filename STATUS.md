# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
<!-- - check-in — api a1b2c3d, web d4e5f6a, app 7b8c9d0 (2026-10-20) -->
- Workflow prepared: brain repo, agents, commands, per-repo Claude settings (2026-10-16)
- Android QA loop: /qa-plan, /qa-run, /qa-retest + scripts/qa toolkit (2026-10-16)

## In progress
- M0 — scaffold done: irbis-api 8fb74fa, irbis-web f6c295f, irbis-app 10701d9. `health` QA: run 2026-10-17_0117 (6 pass / 3 fail),
  retest run 2026-10-17_0127 (3 pass). health/D2 fixed. Waiting on owner: health/D1 decision, `irbis-web/.env.local`.

## Next
- Reference feature `health`

## Known issues
- health/D1 — API chip turns red when only the database is down (4 - Low) — owner to confirm expected behaviour
