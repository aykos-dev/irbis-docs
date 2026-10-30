# Status

Updated by `/feature` and `/bugfix` at wrap-up. Keep it short: one line per item.

## Done
- badges + profile + search (2026-10-30): one local stacked branch chain per api/app/docs, not merged and nothing
  pushed: `feat/badges` → `feat/profile-phase1` → `feat/search`. Badges ships 64 (15 places + 12 regions + 8
  seasons + 10 social + 19 milestones); the canvas names 45, so the owner-approved Milestones group fills 19.
  Release cutoff is `badges.config.startAt`, four earned showcase picks, no XP/gems. Profile implements the
  approved 8-AC app surfaces, gallery-only avatar via `react-native-image-picker`, public profiles, preferences,
  empty notifications and delete-account; search always shows All/Places/People/Groups/Tours, with public + findable
  people only and Groups/Tours coming soon. API `66a3286` → `56f3681` → `bb1c577`; app `a7912eb` → `5530049` →
  `2e76ab0` + `acbe09f`; docs `cc56fb7` → `ec6128e` → final search commit. API check green (53 unit suites / 294
  tests, 30 e2e suites / 234 tests). App lint/typecheck/slop green; 467/471 tests pass, with the same 4 failures
  caused by the owner's uncommitted Crocodile/Imposter word-pack edits. Badge/profile/search copy is agent-drafted;
  owner review and iOS/device QA pending.
- check-in + streaks (2026-10-30): one branch chain per repo, not merged, nothing pushed. api `feat/check-in`
  d4f2ebe check-in endpoint (GPS radius per type, 40–120 XP once per place per Tashkent month, level fact, path
  visit), b7ef93c + 427b027 demo accounts (ADR-006: `POST /v1/auth/demo`, `POST /v1/me/secure` with terms) → api
  `feat/streaks` 75a03b2 flame / boot / 2 shared freezes a month + `GET /v1/me/streaks`, 114d619 admin tie-break
  test timestamp (owner-approved), 9c1c199 weather shield (Sat/Sun 12:00 snapshot job). app `feat/check-in` c900739
  Check in button + offline queue + Summit, 46e921b guest check-ins → demo account + Secure your account → app
  `feat/streaks` 8c0a3a9 Path chips, streak sheet, Summit week tile, lessons line, Profile row. api check green;
  app green except the known pack failures. Manual test by owner pending: AC1–AC8 (check-in), AC1–AC7 (streaks),
  Android + iOS.
- open-bug fixes (2026-10-29), branch `fix/open-bugs-1029` in each repo, not merged, nothing pushed:
  app (from `fix/owner-1022`) 9d4078c Home-card check-out clears track / waypoint queue / SOS contact, f71d857
  plan footnote waits for the contact (fixes flaky plan.test AC4, 6/6 runs green) · api (from `feat/active-trip`)
  ba70721 failed SOS sends start no cooldown (+ e2e) · web (from `feat/active-trip`) ab24793 live page tab title in
  the visitor's language; d641eda XO-1 test presses Stay on the "Leave the game?" sheet (owner-approved test edit,
  assertions unchanged). `npm run check` green in api, web and app (app: 452/452 without the owner's uncommitted
  word-pack edits).
- active-trip (2026-10-21): ActiveTrip screen (map, live km / climb / elapsed, foreground tracking), 5-min location
  pings, public live link + irbis-web page `/t/{token}`, free waypoint check-ins (+10 XP, 500 m / 10 min / max 5,
  offline queue), SOS 3 s hold (server SMS, offline SMS app, call button to `SOS_CALL_NUMBER`), check out + summary.
  api `feat/active-trip` 3ef742c, 6139f92 · app `feat/active-trip` 1588a6c, a85febe · web `feat/active-trip` 89d75c4
  · docs 013a3f9. Branches stack on `feat/trip-plan` (api, app). Manual test by owner pending.
- trip-plan (2026-10-21): plan from Place ("Start adventure"), date/time pickers, sunset buffer, emergency contact
  (encrypted, prefilled), server gear rules, save ahead or start (one active), share sheet, start location fix, Home
  trip card (check-out, change return time, planned start/edit/delete), auto-alert SMS job at back-by + 60 min.
  api `feat/trip-plan` d932b6e, c584a24 · app `feat/trip-plan` 0a1e89f, 298c0aa · docs 3d88dc1. Manual test by owner pending.
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
- conditions — merged to main 2026-10-19 (fast-forward, owner Q9 of campfire-core); was on `feat/conditions` (api 44e08b5, 2e52ef3, 7974da3 · web f84fc3f · app 92887f9, D1 fixes
  c01c7e5, 23e2895, 4eaca16 → 70998f6). Hourly Open-Meteo job + status rules, public condition endpoint, admin
  closures/overrides/recompute, web Conditions page, app condition card + weather + hazards now + Explore chips.
  QA: core 7/7 P0 pass (run 1216 + TC-009 retest 1320), D1 fixed; full run not done. From now on testing is manual
  by the owner (Q13). Owner checks pending: AC1–AC8 by hand, web admin, iOS (2026-10-18)

- levels — merged to main 2026-10-19 (fast-forward); was on `feat/levels` (api 841e4c6, 4f051a5, bd33bdd · app 302b72e,
  2fb47df · web no change). XP ledger + GameConfig (levels.table, xp.dailyCaps) + level engine + LevelFact counters for
  lessons/check-ins/spots; /v1/levels, /v1/me/level, level-up seen, QA grant (`QA_TOOLS_ENABLED`); optional auth on
  public routes; real level on Place, /v1/me and admin users. App: Level, Companions, LevelUp (placeholder evolution),
  Profile badge, Explore lock chips, `irbis://debug/levels/grant`. Manual test by owner pending: AC1–AC8, iOS (2026-10-18)

- campfire-core — on irbis-app `feat/campfire-core` (from main), not merged (app a15a377, 78b24b7, 8d198e7, a15d20a ·
  api/web no change). Community tab = Feed · Groups (coming soon) · Campfire games; CampHub (games, trip group, badges
  coming soon), player sheet, Android local-only hotspot (native CampNet) or Wi-Fi host, iOS Personal Hotspot guide,
  TCP room server :47821 + zeroconf, QR / code join (Bonjour → /24 scan), live lobby (15 incl. host, remove, close),
  reconnect same seat, host resume 12 h, battery ≤20% banner. 248/248 tests. Manual test by owner pending: AC1–AC8 on
  two+ Android phones and iOS (2026-10-19)

- campfire-party — on irbis-app `feat/campfire-party` (from `feat/campfire-core`), not merged (app 7a2e344, 19b8710,
  a11e606, 5c135c1 · api/web no change). Protocol v2; lobby game picker + settings; Imposter (hold-to-reveal word /
  imposter card, host Reveal + New round), Who am I? (others' characters, Show mine), Would you rather (20 per round,
  live count, reveal bars, defend line); Android FLAG_SECURE, iOS capture cover; 8 bundled uz/ru/en packs, no repeats
  per pack on the host phone. No XP / badges (owner). 276/276 tests. Manual test by owner pending: AC1–AC8 on 3+
  Android phones and iOS (2026-10-19)

- campfire-mafia — on irbis-app `feat/campfire-mafia` (from `feat/campfire-party`), not merged (app 283c98c, e0fb351,
  92d28b7, 1f521f6 · api/web no change). Protocol v3; Mafia setup (11 roles, civilians auto-fill, balance hint, reveal
  role when out), random deal (host = narrator, no role), hold-to-reveal role card + I'm ready, host control (killed /
  exiled / back, Night/Day steps), player out list + out banner, win suggestion (maniac → town → mafia) + Game over
  with all roles, Play again. `npm run android:apk` (devRelease + Wi-Fi QR via scripts/serve-apk.js), real app icon
  (Android legacy/round/adaptive, iOS set). No XP / badges. 303/303 tests. Manual test by owner pending: AC1–AC8 on
  6+ phones (5 players + host) and iOS (2026-10-19)

- camp camera (CampJoin QR scan) — fixed on irbis-app `fix/camp-camera` (from `feat/campfire-mafia`), app b34714e:
  first tap shows the OS camera dialog (Android reports 'denied' before any request), Settings only after a denied
  request; `VisionCamera_enableCodeScanner=true` (ML Kit was not linked → black preview) + R8 keep rules for
  VisionCamera/CameraX/ML Kit. 306/306 tests; 1 join test edited (owner, 2026-10-20). Owner check on phone pending:
  release APK scan works (2026-10-20)

- lessons-admin — on `feat/lessons-admin` in api + web (from main), not merged (api bdbf013, 37604ab, 30a5c39 ·
  web e7f98b3, 3eba4ed · app no change). Admin API for tiers → lessons → questions (uz/ru/en, publish rules 5–15
  questions, all locales), question images via api → MinIO/S3 (ADR-005, sharp re-encode, EXIF stripped), level tier
  gates = published lessons per tier (empty tier blocks its gate), 6 tiers + 18 Claude-drafted draft lessons (180 Q).
  Web: Lessons tiers page, tier page, lesson editor. api 163 unit + 165 e2e, web 65 tests green. Manual test by owner
  pending: AC1–AC8 in the admin panel (2026-10-20)

- lessons — on `feat/lessons` in api + app (from main; lessons-admin fast-forwarded into main first, Q14), not merged
  (api ddfbb98 · app 3472e0e, 429861c, 1a96a46, 4c6acc8 · web no change). Public catalog + lesson detail, server-graded
  completions (10 / 15 XP once, level fact, daily goal), guest-merge `lessons`; app LessonsHub (goal ring, tiers, START),
  daily hearts on the phone (5 / Tashkent day), Quiz (re-ask wrong, sheets, haptics + Kenney CC0 sounds, mute), practice
  replays, lesson complete, offline lesson cache + completion queue, LevelUp "Next: <tier>" line. api 170 unit + 172 e2e,
  app 235/235 green; 1 shell test edited (Q16). Manual test by owner pending: AC1–AC8 on Android, iOS (2026-10-20)

- weekly-path — on `feat/weekly-path` in api + app (from main after Q9 merges), not merged (api 6cdfbe9, 8741af9 · app
  d8ffee6, 0e066b9, 196ae8e · web no change). Monthly path (owner Q1): 3 places by level / interests / season, nearest
  Tashkent, frozen per Tashkent month (guests rebuilt from phone interests), live weekend status rings, smart swap
  suggest-only card, done nodes via `recordVisit` (QA route + `irbis://debug/path/visit/<placeId>` until check-in),
  monthly chest +50 XP (`path.config`), Fri–Sun Tashkent weather (PathWeatherJob). api 184 unit + 179 e2e, app 349/349
  green; 4 app tests edited (Q11). Manual test by owner pending: AC1–AC8 on Android, iOS (2026-10-20)
- merges (owner Q9 of weekly-path, 2026-10-20): api main = ddfbb98 (lessons); app main = f7290a3 (campfire-core →
  party → mafia → camp-camera fast-forward, then lessons merge; shell AC1 test edited, Q10)

- campfire-xo — on irbis-app `feat/campfire-xo` (from main), not merged (app e1adc61, 8aad34f · api/web no change).
  Protocol v4; X and O tile (host + exactly 1 joiner), shared 3×3 board, host-validated turns, 8-line win / draw,
  "Next game" by either player (X/O swap, X first), score bar + draws, pause on joiner drop / resume same seat, host
  End → Final score (win / lose / tie, confetti, Play again / Lobby); lessons sound player moved to `src/shared/sounds`
  (win/lose/draw clips + shared mute). No XP / badges. 347/347 tests; 12 campfire-core tests edited for protocol v4
  only. Manual test by owner pending: AC1–AC8 on 2 Android phones, iOS (2026-10-20)

- campfire-crocodile — on irbis-app `feat/campfire-crocodile` (from main), not merged (app 2659073, 1867acb · api/web no
  change). Protocol v5 (v4 = campfire-xo); Crocodile tile (3–15 incl. host), lobby timer 30/60/90 s + pack ticks,
  host picks who shows, hold-to-reveal word (capture blocked) + Skip / Start, timer on all phones (host decides
  time-up, warning last 10 s, haptics last 5 s), Guessed! / Time's up! with the word, describer drop → turn cancelled,
  host End → group summary (guessed · skipped · turns) + Play again / Lobby. Mime only, no score, no sounds, no XP.
  354/354 tests; 12 campfire tests edited for protocol 3 → 5 only. Manual test by owner pending: AC1–AC8 on 3+
  Android phones, iOS (2026-10-20)

- campfire-art — owner art swapped in irbis-app (2026-10-20): `fix/campfire-art` from main (e1b1346: CampHub cheering
  fox, iPhone hotspot picture, Sniper/Journalist/Immortal glyphs, 11 Mafia role card illustrations on the role card),
  `feat/campfire-xo` 76654d4 (XO tile glyph), `feat/campfire-crocodile` d3a398e (Crocodile tile glyph). Checks green
  (332 / 348 / 355 tests), no test edited. Manual check by owner pending: CampHub, iPhone guide, Mafia role card, XO and
  Crocodile tiles on device

- campfire bug fixes — irbis-app `fix/campfire-bugs` from `feat/campfire-crocodile` (e4ab3a3) and
  `fix/campfire-bugs-xo` from `feat/campfire-xo` (07396bd, XO regression test 9213400): CORE-1..3, MAF-1..2 and
  XO-1 from `qa/campfire-games/BUG-REPORT.md`. Joining waits for the native connect (no crash, no false "Room not
  found"), last host messages flush before hang-up, freed seat tokens stay removed, Mafia night exits read
  `left · Night n` with a name/avatar snapshot, and the XO joiner's Back no longer leaves the running board.
  `npm run check` green (72 suites, 360 tests on the crocodile fix branch; 72 suites, 354 tests on the XO fix
  branch). Nothing pushed; owner phone retest pending

## In progress
- (none)

## Next
- campfire-party-2 — pass-and-play (one phone) for Imposter / Who am I / Would you rather + campfire badges + campfire XP (split from campfire-party, Q1)
- places-admin — web CRUD for places (split from places, Q1)
- onboarding-quiz — experienced-user safety quiz (split from onboarding, Q5); after `lessons`, needs a new ADR on what passing grants

## Known issues
- check-in / streaks: art placeholders — Summit uses the fox cheering pose (L3) or neutral companions, streak sheet
  uses worried Irbis for "broken" (sad pose not in the app yet) → prompts in `design/media/IMAGE-PROMPTS.md` § F;
  `checkInRadiusM` only on place detail (list e2e asserts exact keys); admin user DTOs have no `isDemo` (same
  reason); Summit → LevelUp relies on the LevelUp host, untested; demo-account cleanup job not built; flaky app test
  `active-trip/waypoint-sos.test.tsx` "AC6: a check-in posts…" (2/13 on base, 5/8 on `feat/streaks`; "Next:
  Waypoint 2" races the XP chip) → `/bugfix`; ru/uz copy is Claude drafts; iOS not built
- irbis-app: uncommitted owner word-pack edits (`croc-*.json`, `imposter-animals.json`) fail 4 campfire tests
  (party, croc ×2 suites) — check is green without them; brief 1022 item 1 (`serve-apk.js` + `env/apk.env`) is
  still uncommitted in the app working tree
- active-trip: owner OK pending for one test assertion edit (app `trip-plan/card.test.tsx:215`, `trip_checked_out`
  gains `from: 'card'`, asked by the brief) and web fixture `test/session.tsx` (new MeResponseDto fields, synthetic
  values); owner adds `# SOS_CALL_NUMBER=+998XXXXXXXXX` to irbis-api `.env.example` (agents can't open `.env*`) and
  the real value to `.env` — no number = no call button; confirm that line is staffed 24/7 (replaces 112); SOS SMS
  goes through the fake SmsSender; `WEB_PUBLIC_URL` must point at a public irbis-web deploy before contacts can open
  links; tracking is foreground only (screen off = no distance); `<html lang>` on the live page
  stays en (content `div` carries the visitor's lang), late badge is yellow, retry text from `common.errors.retry`; summary shows "+0 XP" when the daily cap
  trims a waypoint; waypoint save +
  XP award are not one transaction (idempotent); ru/uz copy is Claude drafts;
  iOS not built (2026-10-21)
- trip-plan: auto-alert goes through the **fake** SmsSender (logs only) — real provider + ADR needed before launch;
  `SmsSender.sendText` added to auth (fake logs user id + text length); "Open it" link on the 409 "trip in progress"
  toast not built (would need the slice-1 plan.test toast assertion changed — owner call); uz/ru copy is Claude drafts (owner review); 72 h max trip and 14 days plan-ahead are Claude caps
  (GameConfig `trip.config`); location accuracy limit 100 km (not 10 km per brief); gear icons fall back to a generic
  check where `Icon` lacks one; datetimepicker 9.2.1 + geolocation need `pod install` — iOS not built; migration SQL
  written by diff (docker compose needs S3 vars), applied fine in e2e; edit mode covered by one card test (2026-10-21)
- campfire games emulator pass (owner ask, 2026-10-20): 67 cases, 61 pass; 6 bugs found in
  `qa/campfire-games/BUG-REPORT.md` — CORE-1 join by code "Room not found" after found, CORE-2 joiner crash
  `No socket with id`, CORE-3 last host message lost (removed player rejoins), XO-1 joiner Back stuck on waiting (major);
  MAF-1 night leave shows "exiled · Day 1", MAF-2 left player loses name/avatar (minor). **All 6 fixed 2026-10-21**
  on `fix/campfire-bugs` (e4ab3a3) and `fix/campfire-bugs-xo` (07396bd, XO test 9213400); checks green, nothing
  pushed. Owner phone retest pending
- campfire-crocodile: 3 word packs (180 words,
  uz/ru/en) are Claude drafts — owner review (famous-people picks, uz spellings e.g. «Nu, pogodi!», "Oppoqoy");
  no sounds (sound player is still in `lessons` on main — add after campfire-xo merges); protocol v5 vs xo v4 —
  whichever merges second bumps again; after a host restart a `ready` turn keeps its describer even if they never
  return (host can only End); timer ring colours unchecked on device; `crocTurn` app test sets `jest.setTimeout(20000)`
  (5 s timeouts under heavy machine load, also seen in levels/places/lessons/auth suites); `mafia/GameOver.tsx`
  exports `Confetti`; iOS not built; `graphify` not on PATH — app graph not refreshed (2026-10-20)
- campfire-xo: copy `camp.games.xoMeta` "2 · 1–5 min"
  (ru/uz) added by the agent — owner OK pending; a third phone sees the Mafia "Game in progress" text for the whole
  series; joiner-side final score / "Waiting for the host" was covered by a component test only (now also an
  integration test on `fix/campfire-bugs-xo`, 9213400); mute stays under the
  `lessons.muted` key (shared with lessons); ConfirmSheet got `cancelLabel`, Mafia `Confetti` exported for reuse;
  iOS not built; `graphify` not on PATH — app graph not refreshed (2026-10-20)
- weekly-path: placeholders — open chest (lid tilt + sparkle), coin shower, rain/sway are Reanimated; swap card shows a
  place-type tile (no place photo in the API); dark ring tints in `shared/constants/colors.ts` (`pathColors`) are agent
  picks not in design.md — owner OK; 3-node + chest layout adapted by Claude (canvas has 7 nodes); mascot / popover
  positions approximate — check on device; chest log-in prompt uses the generic `xp` reason ("Keep your XP"), not
  "Keep your chest XP"; coin shower only plays when Path is open as the node flips; done only via QA visit until
  `check-in` calls `WeeklyPathService.recordVisit`; check-in at a swap place doesn't count toward the chest; weather
  strip + ranking use Tashkent; Product Overview + canvas still say weekly / 7 nodes — owner updates the doc;
  `path.offline` copy added (not in brief); Tashkent weather uses its own hourly Open-Meteo call (not the conditions
  batch); app d8ffee6 message says check red (fixed by 0e066b9); api e2e Postgres containers time out under heavy load
  (rerun passes) (2026-10-20)
- lessons: nothing shows in the app until the owner publishes lessons (all 18 seeds are drafts) — empty hub until then;
  missing cheering poses (L2, L4–L7), concerned poses and the completion burst are placeholders (neutral + Reanimated) —
  swap when files land in `design/media/lessons/`; correct sheet uses teal AppButton (no green variant); iOS: no
  `pod install` for `react-native-audio-api` 0.13.6 (iOS sound untested), Android has no silent-switch check (media
  volume); hearts don't sync across devices (by design, Q9); question images only cached by RN Image (offline may hide
  them); api completion = award → fact → row without one transaction (all idempotent); GuestMergeDto.lessons only
  shape-checked (handler validates); slice-4 touched shared `guestStore.ts` + `auth.tsx` (onMerged / notifySignInSettled);
  fallback copy `levels.up.tierName` / `tierFirstAid` (uz/ru/en) needs owner OK; untested: hub day flip while open,
  200-item guest cap, foreground sync trigger, LevelUp line in ru/uz; Jest "worker failed to exit" warning seen once,
  not from lessons; `graphify` not on PATH — graphs not refreshed (2026-10-20)
- lessons-admin: 18 draft lessons (180 questions, uz/ru/en) are Claude drafts — owner review before publishing;
  until a tier has published lessons its level gate is unmet (L3+ cannot be reached), seed tiers' `levels.table` sizes
  are now ignored. Owner fills `S3_*` in irbis-api `.env` and runs `docker compose up -d minio minio-init`; MinIO
  images on `latest` (Q10); orphan uploads not cleaned. Test edits: 3 approved (Q9) + levels.e2e setup-only (Q10);
  web `test/session.tsx` ADMIN_ME fixture got `level`/`xpTotal` after gen:api without asking (no assertion change).
  Editor unsaved-guard misses programmatic `router.push`; "Remove its lessons first" uses native `title` tooltip.
  `graphify` not on PATH in the session shell — graphs not refreshed for api/web (2026-10-20)
- campfire-mafia: role texts uz/ru are Claude drafts — owner review pending; balance thresholds (floor(n/4)..floor(n/3)) and default
  counts are guesses; mid-game join "Game in progress" text has no UI test; no " (you)" marker on Game over;
  End game keeps testID `camp.game.end` (not `maf.end`); 1 campfire-core test edited for protocol v3 + 3 for the
  live Mafia tile + 1 type rename (slice 1), 1 mafia test edited (Q9); iOS icon set generated, iOS not built;
  serve-apk has no automated test (2026-10-19)
- irbis-app flaky whoami test (names with brackets in RegExp) fixed 2026-10-21: `fix/whoami-test-regex` 0c3bf77 (from main), cherry-picked to `feat/active-trip` e3987d7 — owner-approved test edit, assertion unchanged
- campfire-party: content packs (design/media/campfire-party/packs, 8 files) are Claude drafts — owner review of
  uz/ru/en wording pending; a few Who am I items repeat Imposter words (plov, camel, snow leopard). Game code lives in
  `src/features/campfire-core/games/` (eslint-boundaries). WYR reveal = one heavy haptic, no drumroll. iOS not built
  (CampCapture/`isCaptured` untested). Player Back on a game screen returns to the lobby while the round runs.
  Unused copy `lobby.start` / `lobby.startSoon` left in camp.json. 5 campfire-core tests edited for protocol v2 (Q10)
  (2026-10-19)
- campfire-core: real phone-to-phone networking only unit-tested with fakes; 10 s silence → "reconnecting…" has no
  test; iOS never built (pods not installed) — CampNet.swift, Hotspot entitlement, vision-camera/wifi-reborn/tcp/zeroconf
  pods untested; vision-camera pinned 4.7.3 (5.x drops Android code scanner); wifi-reborn built via
  `android/third-party-gradle/react-native-wifi-reborn.gradle` (its own gradle fails on Gradle 9.4.1) — recheck on
  Gradle/RN upgrades; device-info API confirmed by typecheck only; `ACCESS_FINE_LOCATION` left uncapped (maps uses it)
  (2026-10-19)
- levels placeholders: LevelUp evolution is a Reanimated sequence — 10 handing/catching poses + `levelup-evolution.json`
  Lottie missing (only fox→ibex art is real); backpack is the onboarding placeholder — swap when the owner drops files in
  `design/media/levels/` (2026-10-18)
- levels: lesson/check-in/spot bars only move via the QA grant until `lessons`, `check-in`, `add-a-spot` call
  `award`/`recordFact`; lesson tier sizes (6, all = 36) are config guesses until `lessons`; `QA_TOOLS_ENABLED` not in
  irbis-api `.env.example` (file permission-blocked) — add by hand; colours #8C5A33, #0B6F6A, #FFD95A used but not in
  design.md; Explore lock uses the live level only (no offline fallback); place refetch on login untested (2026-10-18)
- irbis-app test harness: `navigate()` in app/__tests__/auth/harness.tsx (sync act) breaks the next test after a
  signed-in one — pre-existing, levels tests work around it; needs `/bugfix` (2026-10-18)
- Place (detail + condition) is memory-only: after an offline app restart it shows the offline message (owner Q12: later, with offline maps / Safety) (2026-10-18)
- conditions (review notes, non-blocking): concurrent override creates could leave two active (no partial unique
  index, api conditions.repository.ts:489); expired override / future-start closure shows source with `text: null`
  until the next hourly run; `COND_STALE_HOURS` unused; `created_by_id` FKs RESTRICT admin hard-delete; web place
  conditions page heading is generic "Place conditions" (fix: `usePlacesGet` for the name) (2026-10-18)
- conditions placeholders: weather glyphs (sun, cloud, rain, storm, wind, snow) — swap when the owner drops files in
  `design/media/conditions/`; Open-Meteo free tier is non-commercial — paid plan before launch
- places placeholders: waterfall + canyon type icons and colours (#2BA3C4, #D9733F, not in design.md) — hero art for all
  7 types is the owner's (app c062e05, 2026-10-18)
- places: map tiles stay light in dark mode (OpenFreeMap liberty style); place descriptions render Markdown as plain text;
  STD-TEXT flags level names on Place as untranslated (false positive); thin line over the last text row at the bottom of
  Place in uz/ru crops — owner to check by eye
- iOS: `@maplibre/maplibre-react-native` 11.5.0 added — pods not installed, iOS map/location untested
- irbis-api admin e2e `GET /v1/admin/users joined=today` (test/admin.e2e-spec.ts:461) fails at 00:11 Tashkent (expected 4, got 0); passed earlier the same day with no code change — likely UTC vs Asia/Tashkent day boundary in auth admin filter or its test; pre-existing, needs `/bugfix` (2026-10-18)
- onboarding placeholders: 4 Lottie files (irbis-wave, irbis-nod, irbis-clap, onb5-reveal) show static art / simple Reanimated; backpack SVG; native launch screen is teal only — swap when the owner drops files in `design/media/onboarding/`
- iOS: `lottie-react-native` 7.5.0 added but `pod install` never run in irbis-app (no Podfile.lock) — iOS build untested
- Guest merge runs once per device: a second account created on the same phone (after sign-out) doesn't get the onboarding choices — revisit with lessons/XP guest data
- Auth QA cases that clear app data must call `irbis://debug/onboarding/done` first (fresh install now opens onboarding)
- auth/D1 irbis:// deep links not delivered on Android (no VIEW intent-filter) — fix bf03271 is in app main, awaiting the owner's manual retest
- STD-TEXT now switches the in-app language via dev/staging link `irbis://debug/lang/<uz|ru|en>` (app 46b279c on feat/auth); re-run STD-TEXT on the auth screens in the full run
- iOS: Info.plist has no `irbis` URL scheme, so deep links won't open the app on iOS — follow-up, not logged as a defect yet
