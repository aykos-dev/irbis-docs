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
- places — merged to main (api 46e03e6, app 18603da). Seed 71 places from data.ts, public
  list + detail, app Explore (MapLibre map, filters, location/Tashkent fallback) + Place. QA: core run 2317 11/12 →
  D1 fixed (retest 2337); full run 2351 32/36 → D2, D3 fixed (retest 0015); TC-012 pins and TC-022 no-fix fallback
  manual for owner; 0 open places defects. Owner checks pending: pins/clusters, real GPS + OS prompt, iOS (2026-10-18)

## In progress
- (none)

## Next
- places-admin — web CRUD for places (split from places, Q1)
- onboarding-quiz — experienced-user safety quiz (split from onboarding, Q5); after `lessons`, needs a new ADR on what passing grants

## Known issues
- places placeholders: waterfall + canyon hero art, type icons and colours (#2BA3C4, #D9733F, not in design.md); camping
  reuses the trail illustration — swap when the owner drops files in `design/media/places/`
- places: map tiles stay light in dark mode (OpenFreeMap liberty style); place descriptions render Markdown as plain text;
  STD-TEXT flags level names on Place as untranslated (false positive); thin line over the last text row at the bottom of
  Place in uz/ru crops — owner to check by eye
- iOS: `@maplibre/maplibre-react-native` 11.5.0 added — pods not installed, iOS map/location untested
- irbis-api admin e2e `GET /v1/admin/users joined=today` (test/admin.e2e-spec.ts:461) fails at 00:11 Tashkent (expected 4, got 0); passed earlier the same day with no code change — likely UTC vs Asia/Tashkent day boundary in auth admin filter or its test; pre-existing, needs `/bugfix` (2026-10-18)
- onboarding placeholders: 4 Lottie files (irbis-wave, irbis-nod, irbis-clap, onb5-reveal) show static art / simple Reanimated; backpack SVG; native launch screen is teal only — swap when the owner drops files in `design/media/onboarding/`
- iOS: `lottie-react-native` 7.5.0 added but `pod install` never run in irbis-app (no Podfile.lock) — iOS build untested
- Guest merge runs once per device: a second account created on the same phone (after sign-out) doesn't get the onboarding choices — revisit with lessons/XP guest data
- Auth QA cases that clear app data must call `irbis://debug/onboarding/done` first (fresh install now opens onboarding)
- auth/D1 irbis:// deep links not delivered on Android (no VIEW intent-filter) — fix committed app bf03271 on feat/auth, awaiting retest (`/qa-retest auth/D1`)
- STD-TEXT now switches the in-app language via dev/staging link `irbis://debug/lang/<uz|ru|en>` (app 46b279c on feat/auth); re-run STD-TEXT on the auth screens in the full run
- iOS: Info.plist has no `irbis` URL scheme, so deep links won't open the app on iOS — follow-up, not logged as a defect yet
