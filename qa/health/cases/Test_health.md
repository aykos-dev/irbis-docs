# Test_health — API status (M0 reference feature)

**Spec:** [features/health.md](../../../features/health.md) (status: Approved) · **Written:** 2026-10-17
**Source of truth:** the spec's acceptance criteria. When the app and an AC disagree, the case keeps the AC's
expected result and the case fails.

## 1. How to read
See `qa/_templates/Test_TEMPLATE.md` §1. Cases run on Android (owner's Galaxy S25 Ultra) against the local API
(`irbis-api` on the Mac, reached through `adb reverse tcp:3000 tcp:3000`). `→ check:` failing = Blocked, never Fail.

## 2. Resources
| Env | What it needs |
|---|---|
| Android | Galaxy S25 Ultra (SM-S938B, Android 16), adb serial RFCY616LFMX; build `uz.irbis.app.dev` devRelease (no Metro) |
| Backend | `irbis-api` `npm run start:dev` on :3000, Postgres 17 container `db` (`docker compose` in irbis-api) |
| Tools | adb, scrcpy, `scripts/qa` toolkit; `docker compose stop/start db` for the degraded case |
| Access | none (health is public; no account) |

## 3. Test data
| ID | What | Value |
|---|---|---|
| API-UP | API + DB running | `curl -s localhost:3000/health` → `"status":"ok"` |
| DB-DOWN | DB container stopped, API running | `cd ../irbis-api && docker compose stop db` → `/health` 503 `"db":"down"` |
| API-GONE | API unreachable from the phone | `adb reverse --remove tcp:3000` |
| OFFLINE | phone offline | `set_network(False, False)` (Wi-Fi + data off; USB adb stays) |

Recipes: restore with `docker compose start db`, `adb reverse tcp:3000 tcp:3000`, `set_network(True, True)`.

## 4. Coverage matrix
**Requirements:** 7 AC → 9 cases (5 Core + 4 Supplementary)

| AC | Requirement (short) | Technique | Core | Supplementary |
|---|---|---|---|---|
| AC1 | Up → ok + db up | EP (up) | TC-001 | — |
| AC2 | DB down → degraded, no hang | EP (db down) | TC-002 | — |
| AC3 | Loading / success / error + retry / offline / pull to refresh | ST (states) | TC-003, TC-004, TC-005 | TC-009 |
| AC4 | uz / ru / en copy | EP (locale) | — | TC-006, TC-007 |
| AC5 | Web card | — (covered by irbis-web tests; not on the phone) | — | — |
| AC6 | Generated hook only | static (code review) | — | — |
| AC7 | `health_checked` QA event | EP | TC-001 (bullet 3), TC-002 (bullet 3) | — |
| — | Standards: dark mode, largest font | EG | — | TC-008, TC-009 |

AC5 and AC6 are verified in irbis-web's tests and in review, not on the device — noted, not waived.

## 5. Group 1 — Core

## ▌ 5.1 Smoke and the main states

### ★ TC-001 · P0 · Status screen shows API and database up
---
**Requirement:** AC1 — API reachable and DB up shows ok · [→ AC1 "returns 200 { status: "ok", db: "up", version, time }"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- API-UP; `adb reverse tcp:3000 tcp:3000` active; phone online

**Steps:**
1. Cold start the app (`relaunch()`) → check: `health.status-card` appears within 10 s

**Expected result** (within 10 s after launch):
- Card `health.status-card` shows `health.api-chip` and `health.db-chip` in the Go style, text "API is up" and "Database is up" — screenshot
- `health.version` shows "v0.0.1" (the API's package version) — screenshot
- Event `health_checked` { status: "ok", db: "up" } — event log

### ★ TC-002 · P1 · Database down shows degraded, not an error
---
**Requirement:** AC2 — DB down returns degraded within 3 s · [→ AC2 "returns 503 { status: "degraded", db: "down", … } within 3 s"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb + docker) · resources: DB-DOWN

**Precondition:**
- App open on the Status screen showing ok (TC-001's postcondition)

**Steps:**
1. `docker compose stop db` → check: `curl` `/health` returns 503 with `"db":"down"`
2. Pull to refresh on the Status screen

**Expected result** (within 5 s after step 2):
- `health.db-chip` shows the Not-now style (red, × icon, label "Database is down" or its equivalent) while `health.api-chip` stays Go — screenshot
- No error state and no `health.retry` button (degraded is data, not an error) — screenshot
- Event `health_checked` { status: "degraded", db: "down" } — event log

**Postcondition:** `docker compose start db` (restore before the next case)

### ★ TC-003 · P1 · API unreachable shows an error with Retry, and Retry recovers
---
**Requirement:** AC3 — error state with Retry · [→ AC3 "on API unreachable an error state with Retry"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: API-GONE, API-UP

**Precondition:**
- API-UP; app open on the Status screen

**Steps:**
1. `adb reverse --remove tcp:3000`, then cold start the app → check: `/health` is unreachable from the phone (no `health_checked` event within 15 s)
2. Wait for the error state (query retries finish)
3. `adb reverse tcp:3000 tcp:3000`, tap `health.retry`

**Expected result** (error within 30 s of step 1; recovery within 10 s of step 3):
- After step 2: plain-language error message and `health.retry` visible; no raw status code or stack — screenshot
- After step 3: the card shows "API is up" again — screenshot
- Event `health_checked` { status: "ok" } after the Retry tap — event log

### ★ TC-004 · P1 · Offline shows a persistent banner and keeps the last result
---
**Requirement:** AC3 — offline banner, cached result kept · [→ AC3 "offline (no network) a persistent offline banner, not a toast"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: OFFLINE

**Precondition:**
- App open on the Status screen showing ok

**Steps:**
1. `set_network(False, False)` → check: `dumpsys connectivity` reports no active network

**Expected result** (within 5 s after step 1, still visible at 15 s):
- `app.offline-banner` visible and still visible after 15 s (persistent, not a toast) — screenshot ×2
- The last result ("API is up") stays visible, marked as possibly out of date — screenshot

**Postcondition:** `set_network(True, True)`; the banner disappears within 10 s

### ★ TC-005 · P2 · Pull to refresh refetches
---
**Requirement:** AC3 — pull to refresh refetches · [→ AC3 "Pull to refresh refetches."](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- App open on the Status screen showing ok, online

**Steps:**
1. Swipe down on the Status screen (pull to refresh)

**Expected result** (within 5 s after step 1):
- A new `health_checked` { status: "ok" } event after the swipe — event log
- The refresh indicator appears and then hides — screenrecord+frames

## 6. Group 2 — Supplementary

## ▌ 6.1 Locale and standards

### ★ TC-006 · P2 · Russian copy
---
**Requirement:** AC4 — uz / ru / en via i18n · [→ AC4 "Copy is in uz / ru / en via i18n keys"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- API-UP

**Steps:**
1. `adb shell cmd locale set-app-locales uz.irbis.app.dev --locales ru`, cold start → check: app relaunched

**Expected result** (within 10 s after launch):
- Every text on the Status screen is Russian, matching `src/shared/i18n/ru` — no English left — screenshot
- Layout does not clip or truncate any Russian label — screenshot

**Postcondition:** `cmd locale set-app-locales uz.irbis.app.dev --locales en`

### ★ TC-007 · P2 · Uzbek copy
---
**Requirement:** AC4 — uz / ru / en via i18n · [→ AC4 "Copy is in uz / ru / en via i18n keys"](../../../features/health.md#acceptance-criteria)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- API-UP

**Steps:**
1. `cmd locale set-app-locales uz.irbis.app.dev --locales uz`, cold start → check: app relaunched

**Expected result** (within 10 s after launch):
- Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz` — screenshot

**Postcondition:** app locale back to `en`

### ★ TC-008 · P3 · Dark mode uses the night tokens
---
**Requirement:** standards §5/§8 — light + dark from tokens · [→ AC3 "safe areas; light + dark from tokens"](../../../features/health.md#required-ui-states-every-touched-client)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- API-UP

**Steps:**
1. `dark_mode(True)`, cold start

**Expected result** (within 10 s after launch):
- Background is the Night token (#131D22) and cards #1C2A30; text readable; chips keep colour + icon + label — screenshot

**Postcondition:** `dark_mode(False)` (session.py down also restores it)

### ★ TC-009 · P3 · Largest font size does not clip the card
---
**Requirement:** standards §12 — legible at the largest font size · [→ AC3 "safe areas"](../../../features/health.md#required-ui-states-every-touched-client)
**Env:** Android · auto (adb) · resources: API-UP

**Precondition:**
- API-UP

**Steps:**
1. `font_scale(2.0)`, cold start

**Expected result** (within 10 s after launch):
- All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh still reachable — screenshot

**Postcondition:** `font_scale(1.0)`
