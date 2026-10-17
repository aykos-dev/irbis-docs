# Run 2026-10-17_1133 — health
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — installed uz.irbis.app.dev irbis-app main b0d7e37
**Backend:** local irbis-api localhost:3000
**Device:** sdk_gphone64_arm64 (Android 15) — note: run without the device session (no phone emulation of density; STD-TEXT set font 1.15 itself). Toolkit fixed afterwards so `runcase new` opens the session.
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** all TC + standards on SCREENS
**Blocked reasons:** —
**Plan:** ../../cases/Test_health.md

## Results
8 Pass (TC-001..005, STD-DARK/OFFLINE/TEXT@status) · 0 Fail · 0 Blocked · 0 Not run

## Defects
None.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | Status screen shows API and database up | Pass | ✅✅✅ | — | [proof/TC-001/](proof/TC-001/) |
| TC-002 | Database down: DB chip Not-now, API chip stays up, no error | Pass | ✅✅✅ | — | [proof/TC-002/](proof/TC-002/) |
| TC-003 | API unreachable shows an error with Retry, and Retry recovers | Pass | ✅✅✅ | — | [proof/TC-003/](proof/TC-003/) |
| TC-004 | Offline shows a persistent banner and keeps the last result | Pass | ✅✅ | — | [proof/TC-004/](proof/TC-004/) |
| TC-005 | Pull to refresh refetches | Pass | ✅✅ | — | [proof/TC-005/](proof/TC-005/) |
| STD-DARK@status | Dark mode uses the night tokens — status | Pass | ✅ | — | [proof/STD-DARK@status/](proof/STD-DARK@status/) |
| STD-OFFLINE@status | Offline shows a persistent banner and keeps the screen — status | Pass | ✅✅ | — | [proof/STD-OFFLINE@status/](proof/STD-OFFLINE@status/) |
| STD-TEXT@status | Copy is translated and layout survives long text — status | Pass | ✅— | — | [proof/STD-TEXT@status/](proof/STD-TEXT@status/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

## Additional observations

## Follow-ups
