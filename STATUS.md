# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
<!-- - check-in — api a1b2c3d, web d4e5f6a, app 7b8c9d0 (2026-10-20) -->
- Workflow prepared: brain repo, agents, commands, per-repo Claude settings (2026-10-16)
- Android QA loop: /qa-plan, /qa-run, /qa-retest + scripts/qa toolkit (2026-10-16); screenshots-only evidence, emulator default with phone emulation (2026-10-17)
- auth — merged to main (api fe8f543, web 900fe79, app 46b279c) with QA incomplete by owner decision: run 1706
  49 pass / 1 fail / 7 blocked. Left untested: TC-040 (auth/D1 retest), TC-035 (needs fresh install), STD-TEXT on
  auth screens (login, signup, forgot, guest-profile, gate, account-profile), full run never done (2026-10-17)
- M0 — api 8fb74fa, web f6c295f, app b0d7e37; `health` QA: phone run 0117 (6/9) → health/D1 + D2 fixed → emulator run 1119 9/9 (2026-10-17)

## In progress
- (none)

## Next
- onboarding — resumed 2026-10-17 (answers Q1–Q4 in `features/onboarding.md`, media in `design/media/onboarding/MEDIA.md`)

## Known issues
- auth/D1 irbis:// deep links not delivered on Android (no VIEW intent-filter) — fix committed app bf03271 on feat/auth, awaiting retest (`/qa-retest auth/D1`)
- STD-TEXT now switches the in-app language via dev/staging link `irbis://debug/lang/<uz|ru|en>` (app 46b279c on feat/auth); re-run STD-TEXT on the auth screens in the full run
- iOS: Info.plist has no `irbis` URL scheme, so deep links won't open the app on iOS — follow-up, not logged as a defect yet
