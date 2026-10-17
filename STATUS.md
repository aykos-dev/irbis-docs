# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
<!-- - check-in — api a1b2c3d, web d4e5f6a, app 7b8c9d0 (2026-10-20) -->
- Workflow prepared: brain repo, agents, commands, per-repo Claude settings (2026-10-16)
- Android QA loop: /qa-plan, /qa-run, /qa-retest + scripts/qa toolkit (2026-10-16); screenshots-only evidence, emulator default with phone emulation (2026-10-17)
- auth — merged to main (api fe8f543, web 900fe79, app 46b279c) with QA incomplete by owner decision: run 1706
  49 pass / 1 fail / 7 blocked. Left untested: TC-040 (auth/D1 retest), TC-035 (needs fresh install), STD-TEXT on
  auth screens (login, signup, forgot, guest-profile, gate, account-profile), full run never done (2026-10-17)
- onboarding — merged to main (api 4471316, app 96e76eb). QA: core 11/11 P0 pass (runs 1850 → 2045 → 2050); full run
  2052 29/35 pass. D1 closed (QA-reset issue), D2 closed not retested, D3 fixed not retested — owner dropped font/scroll
  QA (STD-TEXT now translation only). Owner manual checks pending: Onb5/selection haptics, first-run preselect on a
  uz/ru device, iOS (2026-10-17)
- M0 — api 8fb74fa, web f6c295f, app b0d7e37; `health` QA: phone run 0117 (6/9) → health/D1 + D2 fixed → emulator run 1119 9/9 (2026-10-17)

## In progress
- places — spec approved, briefs 1 (api) · 2 (app Place) · 3 (app Explore) (2026-10-17)

## Next
- onboarding-quiz — experienced-user safety quiz (split from onboarding, Q5); after `lessons`, needs a new ADR on what passing grants

## Known issues
- places/D2 (back dead after cold deep link) + D3 (uz level-lock text overflow) — fixes committed app c9365a1 / feadf6e on feat/places, awaiting retest (`/qa-retest places/D2 places/D3`)
- irbis-api admin e2e `GET /v1/admin/users joined=today` (test/admin.e2e-spec.ts:461) fails at 00:11 Tashkent (expected 4, got 0); passed earlier the same day with no code change — likely UTC vs Asia/Tashkent day boundary in auth admin filter or its test; pre-existing, needs `/bugfix` (2026-10-18)
- places/D1 Explore empty state blank after a no-match filter — fix committed app 601a6d4 on feat/places, awaiting retest (`/qa-retest places/D1`)
- onboarding placeholders: 4 Lottie files (irbis-wave, irbis-nod, irbis-clap, onb5-reveal) show static art / simple Reanimated; backpack SVG; native launch screen is teal only — swap when the owner drops files in `design/media/onboarding/`
- iOS: `lottie-react-native` 7.5.0 added but `pod install` never run in irbis-app (no Podfile.lock) — iOS build untested
- Guest merge runs once per device: a second account created on the same phone (after sign-out) doesn't get the onboarding choices — revisit with lessons/XP guest data
- Auth QA cases that clear app data must call `irbis://debug/onboarding/done` first (fresh install now opens onboarding)
- auth/D1 irbis:// deep links not delivered on Android (no VIEW intent-filter) — fix committed app bf03271 on feat/auth, awaiting retest (`/qa-retest auth/D1`)
- STD-TEXT now switches the in-app language via dev/staging link `irbis://debug/lang/<uz|ru|en>` (app 46b279c on feat/auth); re-run STD-TEXT on the auth screens in the full run
- iOS: Info.plist has no `irbis` URL scheme, so deep links won't open the app on iOS — follow-up, not logged as a defect yet
