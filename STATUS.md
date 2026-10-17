# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
<!-- - check-in — api a1b2c3d, web d4e5f6a, app 7b8c9d0 (2026-10-20) -->
- Workflow prepared: brain repo, agents, commands, per-repo Claude settings (2026-10-16)
- Android QA loop: /qa-plan, /qa-run, /qa-retest + scripts/qa toolkit (2026-10-16); screenshots-only evidence, emulator default with phone emulation (2026-10-17)
- M0 — api 8fb74fa, web f6c295f, app b0d7e37; `health` QA: phone run 0117 (6/9) → health/D1 + D2 fixed → emulator run 1119 9/9 (2026-10-17)

## In progress
- auth — built + reviewed (PASS) on `feat/auth`: api fe8f543, app 1a4978d, web 900fe79 (not merged). QA plan: 39 cases
  (19 P0). Next, in a FRESH session: `/qa-run auth installed` (core = P0, app build 4c563f2 installed) → bugfix/retest
  loop → `/qa-run auth installed full` → merge feat/auth → wrap up. 1st attempt (2026-10-17) stopped after 72 min;
  unreviewed fails then: TC-003, 035, 037, 040, 041, 042. QA sped up: core/full scope, no timer waits, per-case reset.
  Owner to-dos: create the first admin with `npm run admin:create` (irbis-api) to try the web panel;
  `irbis-web/.env.local`. Real SMS provider: later (staging can't boot until its adapter exists).

## Next
- onboarding — paused before spec; answers Q1–Q4 in `features/onboarding.md`, media list in
  `design/media/onboarding/MEDIA.md`. Resume with `/feature onboarding` after auth is merged.

## Known issues
- auth/D1 irbis:// deep links not delivered on Android (no VIEW intent-filter) — fix committed app bf03271 on feat/auth, awaiting retest (`/qa-retest auth/D1`)
- iOS: Info.plist has no `irbis` URL scheme, so deep links won't open the app on iOS — follow-up, not logged as a defect yet
