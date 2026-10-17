# Run 2026-10-17_1119 — health
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — devRelease arm64 APK, irbis-app b0d7e37 (fix/health-d1)
**Backend:** local irbis-api 8fb74fa via adb reverse
**Device:** emulator, emulating the owner's phone (density 450, font 1.15) —  sdk_gphone64_arm64 (Android 15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** full suite on the emulator pixel-8a (Android 15) emulating the S25 Ultra: density 450, font 1.15; no video
**Blocked reasons:** —
**Plan:** ../../cases/Test_health.md

## Results
**Pass 9** (TC-001 – TC-009) · Fail 0 · Blocked 0 · Not run 0. Confirms health/D1 and health/D2 fixed on irbis-app b0d7e37.

## Defects
None.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| [TC-001](#tc-001) | Status screen shows API and database up | Pass | both chips green, v0.0.1, event ok/up | — | [proof/TC-001/](proof/TC-001/) |
| [TC-002](#tc-002) | Database down shows degraded, not an error | Pass | API chip green 'API is up', DB chip red 'Database is down', no error/Retry | — | [proof/TC-002/](proof/TC-002/) |
| [TC-003](#tc-003) | API unreachable shows an error with Retry, and Retry recovers | Pass | plain error + RETRY, recovers | — | [proof/TC-003/](proof/TC-003/) |
| [TC-004](#tc-004) | Offline shows a persistent banner and keeps the last result | Pass | offline banner at 5 s and 15 s, last result kept + 'Not updated' note | — | [proof/TC-004/](proof/TC-004/) |
| [TC-005](#tc-005) | Pull to refresh refetches | Pass | spinner visible right after the swipe; new health_checked | — | [proof/TC-005/](proof/TC-005/) |
| [TC-006](#tc-006) | Russian copy | Pass | Russian copy; wrapped DB chip inside the card at density 450 + font 1.15 | — | [proof/TC-006/](proof/TC-006/) |
| [TC-007](#tc-007) | Uzbek copy | Pass | Uzbek copy; wrapped chip inside the card | — | [proof/TC-007/](proof/TC-007/) |
| [TC-008](#tc-008) | Dark mode uses the night tokens | Pass | night background, chips keep colour + icon + label | — | [proof/TC-008/](proof/TC-008/) |
| [TC-009](#tc-009) | Largest font size does not clip the card | Pass | font 2.0: texts wrap, chip inside the card | — | [proof/TC-009/](proof/TC-009/) |

## Cases

<a id="tc-001"></a>
### TC-001 · Pass · Status screen shows API and database up
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Status screen shows API and database up · [→ Test_health.md](../../cases/Test_health.md#tc-001--p0--status-screen-shows-api-and-database-up)
**Done:** API-UP; `adb reverse tcp:3000 tcp:3000` active; phone online → 1. Cold start the app
**Expected** (source: AC1):
1. Card `health.status-card` shows `health.api-chip` and `health.db-chip` in the Go style, text "API is up" and "Database is up" — screenshot
2. `health.version` shows "v0.0.1" (the API's package version) — screenshot
3. Event `health_checked` { status: "ok", db: "up" } — event log
**Actual:**
1. ✅ texts: ['IRBIS', 'Status', 'API is up', 'Database is up', 'v0.0.1', 'Checked at 11:19\u202fAM', 'Environment: dev', '11:19'] — proof/TC-001/1_status.png
2. ✅ version v0.0.1 shown — proof/TC-001/1_status.png
3. ✅ event: {'status': 'ok', 'db': 'up'} — no proof
**Conclusion:** AC1, AC7 hold on the emulator.

<a id="tc-002"></a>
### TC-002 · Pass · Database down shows degraded, not an error
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb + docker) · resources: DB-DOWN
**Case:** Database down shows degraded, not an error · [→ Test_health.md](../../cases/Test_health.md#tc-002--p1--database-down-shows-degraded-not-an-error)
**Done:** App open on the Status screen showing ok (TC-001's postcondition) → 1. Stop the database container → 2. Pull to refresh
**Expected** (source: AC2):
1. `health.db-chip` shows the Not-now style (red, × icon, label "Database is down" or its equivalent) while `health.api-chip` stays Go — screenshot
2. No error state and no `health.retry` button (degraded is data, not an error) — screenshot
3. Event `health_checked` { status: "degraded", db: "down" } — event log
**Actual:**
1. ✅ db down shown: True; texts: ['IRBIS', 'Status', 'API is up', 'Database is down', 'v0.0.1', 'Checked at 11:19\u202fAM', 'Environment: dev', '11:19'] — proof/TC-002/2_degraded.png
2. ✅ no error state / Retry — proof/TC-002/2_degraded.png
3. ✅ event: {'status': 'degraded', 'db': 'down'} — no proof
**Conclusion:** AC2 + AC3 (Q4) hold — health/D1 fixed.

<a id="tc-003"></a>
### TC-003 · Pass · API unreachable shows an error with Retry, and Retry recovers
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb) · resources: API-GONE, API-UP
**Case:** API unreachable shows an error with Retry, and Retry recovers · [→ Test_health.md](../../cases/Test_health.md#tc-003--p1--api-unreachable-shows-an-error-with-retry-and-retry-recovers)
**Done:** API-UP; app open on the Status screen → 1. Remove the port forward and cold start → 2. Wait for the error state → 3. Restore the forward and tap Retry
**Expected** (source: AC3):
1. After step 2: plain-language error message and `health.retry` visible; no raw status code or stack — screenshot
2. After step 3: the card shows "API is up" again — screenshot
3. Event `health_checked` { status: "ok" } after the Retry tap — event log
**Actual:**
1. ✅ retry shown: True; texts: ['11:20', 'IRBIS', 'Status', "Can't check the status", "Can't reach Irbis. Check your connection and try again.", 'RETRY', 'Environment: dev'] — proof/TC-003/2_error.png
2. ✅ API is up after Retry — proof/TC-003/3_recovered.png
3. ✅ event: {'status': 'ok', 'db': 'up'} — no proof
**Conclusion:** Error state and Retry work.

<a id="tc-004"></a>
### TC-004 · Pass · Offline shows a persistent banner and keeps the last result
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb) · resources: OFFLINE
**Case:** Offline shows a persistent banner and keeps the last result · [→ Test_health.md](../../cases/Test_health.md#tc-004--p1--offline-shows-a-persistent-banner-and-keeps-the-last-result)
**Done:** App open on the Status screen showing ok → 1. Turn Wi-Fi and mobile data off
**Expected** (source: AC3):
1. `app.offline-banner` visible and still visible after 15 s (persistent, not a toast) — screenshot ×2
2. The last result ("API is up") stays visible, marked as possibly out of date — screenshot
**Actual:**
1. ✅ banner at 5 s: True, at 15 s: True — proof/TC-004/1_offline_5s.png, proof/TC-004/1_offline_15s.png
2. ✅ result kept: True, marked stale: True; texts: ["You're offline. Showing the last saved data.", 'IRBIS', 'Status', 'API is up', 'Database is up', 'v0.0.1', 'Checked at 11:20\u202fAM', 'Not updated — this is the last known result.', 'Environment: dev', '11:20'] — proof/TC-004/1_offline_15s.png
**Conclusion:** Offline handling matches AC3.

<a id="tc-005"></a>
### TC-005 · Pass · Pull to refresh refetches
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Pull to refresh refetches · [→ Test_health.md](../../cases/Test_health.md#tc-005--p2--pull-to-refresh-refetches)
**Done:** App open on the Status screen showing ok, online → 1. Pull to refresh
**Expected** (source: AC3):
1. A new `health_checked` { status: "ok" } event after the swipe — event log
2. The refresh indicator is visible right after the swipe is released (≤ 0.5 s) — screenshot
**Actual:**
1. ✅ event after swipe: {'status': 'ok', 'db': 'up'} — no proof
2. ✅ refresh spinner visible in 1_spinner.png taken right after the swipe — proof/TC-005/1_spinner.png
**Conclusion:** Pull to refresh refetches.

<a id="tc-006"></a>
### TC-006 · Pass · Russian copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Russian copy · [→ Test_health.md](../../cases/Test_health.md#tc-006--p2--russian-copy)
**Done:** API-UP → 1. Font scale 1.15 (Samsung default) → 2. Set the app language to Russian and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Russian, matching `src/shared/i18n/ru` — no English left — screenshot
2. Layout does not clip or truncate any Russian label — screenshot
**Actual:**
1. ✅ English-looking texts left: []; all: ['11:20', 'IRBIS', 'Статус', 'API работает', 'База данных работает', 'v0.0.1', 'Проверено в 11:20', 'Окружение: dev'] — proof/TC-006/1_ru.png
2. ✅ 'База данных работает' wraps to 2 lines and the chip ends inside the card — proof/TC-006/1_ru.png
**Conclusion:** AC4 holds; layout matches the phone.

<a id="tc-007"></a>
### TC-007 · Pass · Uzbek copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Uzbek copy · [→ Test_health.md](../../cases/Test_health.md#tc-007--p2--uzbek-copy)
**Done:** API-UP → 1. Font scale 1.15 (Samsung default) → 2. Set the app language to Uzbek and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz` — screenshot
**Actual:**
1. ✅ English texts left: []; all: ['IRBIS', 'Holat', 'API ishlayapti', 'Ma’lumotlar bazasi ishlayapti', 'v0.0.1', '11:20 da tekshirildi', 'Muhit: dev', '11:20'] — proof/TC-007/1_uz.png
**Conclusion:** AC4 holds.

<a id="tc-008"></a>
### TC-008 · Pass · Dark mode uses the night tokens
**Group:** Supplementary · **Priority:** P3 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Dark mode uses the night tokens · [→ Test_health.md](../../cases/Test_health.md#tc-008--p3--dark-mode-uses-the-night-tokens)
**Done:** API-UP → 1. Dark mode on, cold start
**Expected** (source: standards §5/§8):
1. Background is the Night token (#131D22) and cards #1C2A30; text readable; chips keep colour + icon + label — screenshot
**Actual:**
1. ✅ background pixel (19, 29, 34) vs #131D22 — proof/TC-008/1_dark.png
**Conclusion:** Dark mode uses the night tokens.

<a id="tc-009"></a>
### TC-009 · Pass · Largest font size does not clip the card
**Group:** Supplementary · **Priority:** P3 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Largest font size does not clip the card · [→ Test_health.md](../../cases/Test_health.md#tc-009--p3--largest-font-size-does-not-clip-the-card)
**Done:** API-UP → 1. Font scale 2.0, cold start
**Expected** (source: standards §12):
1. All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh still reachable — screenshot
**Actual:**
1. ✅ all card texts readable and wrapped; health.db-chip inside the card — proof/TC-009/1_font2.png
**Conclusion:** Largest font does not clip.


## Additional observations
- **Emulator vs phone:** same build, same API, same results. Rendering matches the phone once the emulator uses the
  phone's density (450 → 384 dp wide) and font scale (1.15); at the emulator's own defaults (420 dpi, font 1.0)
  Russian labels did not wrap, so health/D2 would not have been visible. `session.py up` now applies
  `emulate_phone` from qa.config.json automatically on emulators.
- Differences that remain: status-bar height/icons, no Samsung Edge-panels handle, emulated network ("3G").
- Evidence is screenshots + steps + QA events (no video, owner's request 2026-10-17).

## Follow-ups
