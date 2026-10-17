# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
<!-- - check-in — api a1b2c3d, web d4e5f6a, app 7b8c9d0 (2026-10-20) -->
- Workflow prepared: brain repo, agents, commands, per-repo Claude settings (2026-10-16)
- Android QA loop: /qa-plan, /qa-run, /qa-retest + scripts/qa toolkit (2026-10-16); screenshots-only evidence, emulator default with phone emulation (2026-10-17)
- M0 — api 8fb74fa, web f6c295f, app b0d7e37; `health` QA: phone run 0117 (6/9) → health/D1 + D2 fixed → emulator run 1119 9/9 (2026-10-17)

## In progress
- auth — built + reviewed (PASS) on `feat/auth`: api fe8f543, app 1a4978d, web 900fe79 (not merged). Next, in a FRESH session
  from irbis-docs: `/qa-plan auth` then `/qa-run auth installed` (emulator; app build 4c563f2 installed) → bugfix/retest
  loop → merge feat/auth → wrap up. First QA attempt stopped at the usage limit (2026-10-17).
  Owner to-dos: create the first admin with `npm run admin:create` (irbis-api) to try the web panel;
  `irbis-web/.env.local`. Real SMS provider: later (staging can't boot until its adapter exists).

## Next

## Known issues
- none
