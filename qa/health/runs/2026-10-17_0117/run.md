# Run 2026-10-17_0117 — health
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — devRelease arm64 APK, irbis-app 2141d96
**Backend:** local irbis-api 8fb74fa via adb reverse
**Device:** SM-S938B (Android 16)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** all 9 cases
**Blocked reasons:** none (first TC-001 attempt was blocked by a toolkit config error — launch activity — fixed and re-run)
**Plan:** ../../cases/Test_health.md

## Results
**Pass 6** (TC-001, TC-003, TC-004, TC-005, TC-007, TC-008) · **Fail 3** (TC-002, TC-006, TC-009) · Blocked 0 · Not run 0.
AC5 (web card) and AC6 (generated hook) verified in irbis-web tests and code review, not on the device.

## Defects
| # | Severity | Defect | Cases | Bug file |
|---|---|---|---|---|
| [D1](#d1) | 4 - Low | API chip turns red when only the database is down | TC-002 | [D1](../../bugs/D1_api-chip-red-when-db-down/D1_api-chip-red-when-db-down.md) |
| [D2](#d2) | 3 - Medium | Status chip runs past the card when its label wraps | TC-006, TC-007 (extra), TC-009 | [D2](../../bugs/D2_wrapped-chip-overflows-card/D2_wrapped-chip-overflows-card.md) |

<a id="d1"></a>
### D1 · Low · API chip turns red when only the database is down
**Path:** API up → database stopped → pull to refresh.
**Expected:** API chip stays "API is up"; only the database chip turns red. manba: AC3 + QA reading (spec silent).
**Actual:** API chip "API is degraded", red ×. **Cause in code:** `HealthCard.tsx:31-33` uses the overall status.
**Warning:** rests on a QA reading — owner to confirm or accept as designed.

<a id="d2"></a>
### D2 · Medium · Status chip runs past the card when its label wraps
**Path:** font 1.15 (this phone's default) + Russian or Uzbek, or English at font 2.0.
**Expected:** chip stays inside the card. manba: AC4, standards §12/§13.
**Actual:** wrapped chip wider than the card. **Cause in code:** `StatusChip.tsx:77-85` (no maxWidth / flexShrink).

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| [TC-001](#tc-001) | Status screen shows API and database up | Pass | both chips green, v0.0.1, event ok/up | — | [proof/TC-001/](proof/TC-001/) |
| [TC-002](#tc-002) | Database down shows degraded, not an error | Fail | DB chip red 'Database is down' (correct) but API chip also red 'API is degraded' | ❌ 1 | [proof/TC-002/](proof/TC-002/) |
| [TC-003](#tc-003) | API unreachable shows an error with Retry, and Retry recovers | Pass | plain error + RETRY, recovers to API is up | — | [proof/TC-003/](proof/TC-003/) |
| [TC-004](#tc-004) | Offline shows a persistent banner and keeps the last result | Pass | offline banner at 5 s and 15 s, last result kept + 'Not updated' note | — | [proof/TC-004/](proof/TC-004/) |
| [TC-005](#tc-005) | Pull to refresh refetches | Pass | new health_checked after swipe; spinner shown then hidden | — | [proof/TC-005/](proof/TC-005/) |
| [TC-006](#tc-006) | Russian copy | Fail | all copy Russian; wrapped 'База данных работает' chip runs past the card's right border | ❌ 2 | [proof/TC-006/](proof/TC-006/) |
| [TC-007](#tc-007) | Uzbek copy | Pass | all copy Uzbek | — | [proof/TC-007/](proof/TC-007/) |
| [TC-008](#tc-008) | Dark mode uses the night tokens | Pass | night background #131D22, chips keep colour + icon + label | — | [proof/TC-008/](proof/TC-008/) |
| [TC-009](#tc-009) | Largest font size does not clip the card | Fail | at font scale 2.0 the 'Database is up' chip runs past the card's right border | ❌ 1 | [proof/TC-009/](proof/TC-009/) |

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
1. ✅ texts: ['IRBIS', 'Status', 'API is up', 'Database is up', 'v0.0.1', 'Checked at 1:18\u202fAM', 'Environment: dev', '01:18'] — proof/TC-001/1_status.png, video.mp4 t=00:02
2. ✅ version v0.0.1 shown — proof/TC-001/1_status.png, video.mp4 t=00:02
3. ✅ event: {'status': 'ok', 'db': 'up'} — video.mp4 t=00:02
**Conclusion:** AC1 and AC7 hold on the device against the real API.

<a id="tc-002"></a>
### TC-002 · Fail · Database down shows degraded, not an error
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb + docker) · resources: DB-DOWN
**Case:** Database down shows degraded, not an error · [→ Test_health.md](../../cases/Test_health.md#tc-002--p1--database-down-shows-degraded-not-an-error)
**Done:** App open on the Status screen showing ok (TC-001's postcondition) → 1. Stop the database container → 2. Pull to refresh
**Expected** (source: AC2):
1. `health.db-chip` shows the Not-now style (red, × icon, label "Database is down" or its equivalent) while `health.api-chip` stays Go — screenshot
2. No error state and no `health.retry` button (degraded is data, not an error) — screenshot
3. Event `health_checked` { status: "degraded", db: "down" } — event log
**Actual:**
1. ❌ health.db-chip red × 'Database is down' (correct); health.api-chip ALSO red × 'API is degraded' — the plan expects it to stay Go because the API responded — proof/TC-002/2_degraded.png, video.mp4 t=00:03
2. ✅ no error state / Retry — proof/TC-002/2_degraded.png, video.mp4 t=00:03
3. ✅ event: {'status': 'degraded', 'db': 'down'} — video.mp4 t=00:03
**Conclusion:** Degraded is shown as data (no error, no Retry) and the event is right, but the API chip turns Not-now although the API answered → D1 (rests on the plan's reading; spec silent on the API chip).

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
1. ✅ retry shown: True; texts: ['IRBIS', 'Status', "Can't check the status", "Can't reach Irbis. Check your connection and try again.", 'RETRY', 'Environment: dev', '01:18'] — proof/TC-003/2_error.png, video.mp4 t=00:16
2. ✅ API is up after Retry — proof/TC-003/3_recovered.png, video.mp4 t=00:17
3. ✅ event: {'status': 'ok', 'db': 'up'} — video.mp4 t=00:17
**Conclusion:** Error state and Retry work; no raw codes shown.

<a id="tc-004"></a>
### TC-004 · Pass · Offline shows a persistent banner and keeps the last result
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb) · resources: OFFLINE
**Case:** Offline shows a persistent banner and keeps the last result · [→ Test_health.md](../../cases/Test_health.md#tc-004--p1--offline-shows-a-persistent-banner-and-keeps-the-last-result)
**Done:** App open on the Status screen showing ok → 1. Turn Wi-Fi and mobile data off
**Expected** (source: AC3):
1. `app.offline-banner` visible and still visible after 15 s (persistent, not a toast) — screenshot ×2
2. The last result ("API is up") stays visible, marked as possibly out of date — screenshot
**Actual:**
1. ✅ banner at 5 s: True, at 15 s: True — proof/TC-004/1_offline_5s.png, proof/TC-004/1_offline_15s.png, video.mp4 t=00:14
2. ✅ result kept: True, marked stale: True; texts: ["You're offline. Showing the last saved data.", 'IRBIS', 'Status', 'API is up', 'Database is up', 'v0.0.1', 'Checked at 1:19\u202fAM', 'Not updated — this is the last known result.', 'Environment: dev', '01:19'] — proof/TC-004/1_offline_15s.png, video.mp4 t=00:14
**Conclusion:** Offline handling matches AC3 and the standards (banner, not toast; cached data marked stale).

<a id="tc-005"></a>
### TC-005 · Pass · Pull to refresh refetches
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Pull to refresh refetches · [→ Test_health.md](../../cases/Test_health.md#tc-005--p2--pull-to-refresh-refetches)
**Done:** App open on the Status screen showing ok, online → 1. Pull to refresh
**Expected** (source: AC3):
1. A new `health_checked` { status: "ok" } event after the swipe — event log
2. The refresh indicator appears and then hides — screenrecord+frames
**Actual:**
1. ✅ event after swipe: {'status': 'ok', 'db': 'up'} — no proof
2. ✅ refresh spinner visible ~0.4–1.0 s after the swipe, then hidden (frames from video t=00:02–00:04) — proof/TC-005/1_after_refresh.png
**Conclusion:** Pull to refresh refetches.

<a id="tc-006"></a>
### TC-006 · Fail · Russian copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Russian copy · [→ Test_health.md](../../cases/Test_health.md#tc-006--p2--russian-copy)
**Done:** API-UP → 1. Set the app language to Russian and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Russian, matching `src/shared/i18n/ru` — no English left — screenshot
2. Layout does not clip or truncate any Russian label — screenshot
**Actual:**
1. ✅ Статус, API работает, База данных работает, Проверено в 01:19, Окружение: dev — no English UI copy ('dev' is the environment value) — proof/TC-006/1_ru.png, video.mp4 t=00:02
2. ❌ health.db-chip wraps to 2 lines and extends past the card's right border — proof/TC-006/1_ru.png, video.mp4 t=00:02
**Conclusion:** Russian copy complete (the script's flag on 'dev' is the environment value, not English). Layout breaks when the chip wraps → D2.

<a id="tc-007"></a>
### TC-007 · Pass · Uzbek copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Uzbek copy · [→ Test_health.md](../../cases/Test_health.md#tc-007--p2--uzbek-copy)
**Done:** API-UP → 1. Set the app language to Uzbek and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz` — screenshot
**Actual:**
1. ✅ English texts left: []; all: ['01:19', 'IRBIS', 'Holat', 'API ishlayapti', 'Ma’lumotlar bazasi ishlayapti', 'v0.0.1', '01:19 da tekshirildi', 'Muhit: dev'] — proof/TC-007/1_uz.png
**Conclusion:** Uzbek copy complete.
**Extra:** The wrapped 'Ma'lumotlar bazasi ishlayapti' chip also runs past the card's right border — same defect as TC-006 (D2).

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
### TC-009 · Fail · Largest font size does not clip the card
**Group:** Supplementary · **Priority:** P3 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Largest font size does not clip the card · [→ Test_health.md](../../cases/Test_health.md#tc-009--p3--largest-font-size-does-not-clip-the-card)
**Done:** API-UP → 1. Font scale 2.0, cold start
**Expected** (source: standards §12):
1. All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh still reachable — screenshot
**Actual:**
1. ❌ card texts readable and wrapped, but health.db-chip extends past the card's right border — proof/TC-009/1_font2.png, video.mp4 t=00:03
**Conclusion:** Text wraps (good) but the chip is wider than the card → D2.


## Additional observations
- The thin bordered sliver at the screen's left edge in every screenshot is Samsung's **Edge panels** handle (system UI), not the app.
- TC-006's script flagged "Окружение: dev" as English — "dev" is the environment value; Russian copy is complete.

## Follow-ups
- Fix with `/bugfix health/D2` (and `/bugfix health/D1` if the owner confirms), rebuild, `/qa-retest health/D1 health/D2`.
- Toolkit: case scripts must keep the failing state on screen until the recording stops (TC-009's last frame shows the
  restored font); fixed in the D2 repro, apply to case scripts on the next edit.
- Session cleanup (`session.py down`): network, font scale (back to 1.15), rotation, show taps, dark mode restored; Do Not Disturb off as before. No test data created (health has none).
