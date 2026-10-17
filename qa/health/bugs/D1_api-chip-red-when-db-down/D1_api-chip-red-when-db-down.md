# D1 · API chip turns red when only the database is down

| | |
|---|---|
| Status | Fixed · retest 2026-10-17 |
| Severity | 4 - Low |
| Feature | [features/health.md](../../../../features/health.md) |
| Found | run [2026-10-17_0117](../../runs/2026-10-17_0117/run.md), TC-002 |
| Build | uz.irbis.app.dev 0.0.1 devRelease arm64, irbis-app commit 2141d96; irbis-api 8fb74fa |
| Retest 2026-10-17 | ✅ Fixed on emulator pixel-8a (Android 15), irbis-app b0d7e37 — [screenshot](image/02_db_down__retest-2026-10-17.png) |
| Video | [D1_api-chip-red-when-db-down.mp4](video/D1_api-chip-red-when-db-down.mp4) (step captions under the screen) |

## Bug

**Title:** [Status / API chip] - API chip shows "API is degraded" in red when only the database is down

**Description**

On the Status screen, when the database is unreachable but the API still answers, both chips turn red: the database
chip correctly says "Database is down", and the API chip also changes to "API is degraded" with the Not-now style. A
reader concludes the API itself is failing, although it responded.

*Reference: features/health.md acceptance criteria AC3: "shows: loading skeleton → "API is up · Database is up · v{version}" with a Go-style chip" (QA reading, owner to confirm — the spec does not say what the API chip shows in the degraded case).*

- **Environment / Build Version:** Galaxy S25 Ultra (Android 16), Irbis app 0.0.1 dev release, local API 0.0.1

**Steps to Reproduce**

1. Run the API and its database; open the app on the Status screen (both chips green).
2. Stop the database, keeping the API running.
3. Pull down to refresh the Status screen.

**Actual Result**

The API chip changes to "API is degraded" (red, × icon) and the database chip shows "Database is down"; the
`health_checked` event reports `{ status: "degraded", db: "down" }`.

**Expected Result**

The API chip stays "API is up" (green) because the API answered; only the database chip turns red.

---

## Internal notes

### Retest 2026-10-17
- **Result:** ✅ Fixed — owner decided the API chip stays green when only the database is down (spec AC3 + Q4).
- **Build:** devRelease arm64, irbis-app `b0d7e37` (branch `fix/health-d1`, merged to main), API `8fb74fa`.
  Device: emulator pixel-8a, Android 15 (no video; screenshots + steps).
- **Code change since the found build (2141d96):** `b0d7e37` (the fix — `HealthCard.tsx` API chip always Go when a
  result exists; `health.apiDegraded` removed in uz/ru/en) and `10701d9` (D2, StatusChip layout) — the old steps reach it.
- **Seen:** API chip "API is up" (green), database chip "Database is down" (red) after the database stopped —
  [image/02_db_down__retest-2026-10-17.png](image/02_db_down__retest-2026-10-17.png); events
  `health_checked {ok, up}` → `{degraded, down}`. Full suite re-run [2026-10-17_1119](../../runs/2026-10-17_1119/run.md): 9/9 pass.
- **Test:** `src/app/__tests__/Status.test.tsx` "AC3 … API chip stays up (Q4, health/D1)" — fails on the old code, passes on the fix.

### Recording
- Re-record: `~/.claude/venvs/qa/bin/python others/repro.py` (retest: `… repro.py retest-YYYY-MM-DD`)
- Video: [video/D1_api-chip-red-when-db-down.mp4](video/D1_api-chip-red-when-db-down.mp4)

| Video time | Caption |
|---|---|
| 00:00 | Setup: API and database running; app language English |
| 00:00 | Step 1: Open the app |
| 00:01 | Step 2: The database stops (API keeps running) |
| 00:02 | Step 3: Pull down to refresh the Status screen |
| 00:05 | Observed: API chip 'API is degraded', database chip 'Database is down' |
| 00:08 | Expected / Result: FAIL |

Events: `health_checked {status: ok, db: up}` → `health_checked {status: degraded, db: down}`.
Screenshots: [image/01_all_up.png](image/01_all_up.png), [image/02_db_down.png](image/02_db_down.png)

### Which AC is broken
- AC3 (QA reading): the API chip should describe the API, not the overall status.
- Cause in code (for the developer): `irbis-app/src/features/health/components/HealthCard.tsx:31-33` derives the API
  chip from `result.status` (overall), not from "the API answered". If the API answered at all, the API is up.

### Why Low
Developer-facing status screen only; no user data or money involved. Misleading, not blocking.

### Decision
Owner, 2026-10-17: keep the API chip green (spec AC3 updated, Q4).
