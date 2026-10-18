# Run 2026-10-18_1216 — conditions
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/conditions 92887f9 devRelease
**Backend:** irbis-api feat/conditions 2e52ef3, CONDITIONS_JOB_ENABLED=false
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** core
**Blocked reasons:** —
**Plan:** ../../cases/Test_conditions.md

## Results
7 Pass (TC-001..006, TC-009) / 0 Fail / 0 Blocked / 0 not run. TC-009 rewritten per Q10 and owner: Explore needs no offline, so only Place is asserted. D1 withdrawn.
6 Pass (TC-001..006) / 1 Fail (TC-009 -> D1) / 0 Blocked / 0 not run. TC-009 rewritten per Q10 (open online, go offline, reopen) and rerun on the same build.
6 Pass (TC-001..006) / 1 Fail (TC-009 -> D1) / 0 Blocked / 0 not run. TC-009 first Blocked, then rewritten per Q10 (open online, go offline, reopen) and rerun on the same build. Case-script fixes during the run (chip text de-dupe, scroll to reason, case-insensitive credit, TASHKENT import); first verdicts were script errors, the app was correct.

## Defects
None (D1 withdrawn, not a defect).
D1 conditions: Explore offline shows connection error, no cached chip (TC-009).
D1 conditions: Explore offline shows connection error, no cached chip (TC-009).

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | Place shows the Go card for a mild weekend: chip, title, age + source, good-weather reason | Pass | ✅✅✅✅ | — | [proof/TC-001/](proof/TC-001/) |
| TC-002 | Closure beats a mild forecast: Not now, admin text (uz fallback in English), worried Irbis | Pass | ✅✅✅✅ | — | [proof/TC-002/](proof/TC-002/) |
| TC-003 | Seasonal lock beats the forecast: 'Closed for the season · Opens in {Month}' | Pass | ✅✅✅ | — | [proof/TC-003/](proof/TC-003/) |
| TC-004 | Weather card: per window day temps, wind + rain chance of the worst day, Open-Meteo credit | Pass | ✅✅✅ | — | [proof/TC-004/](proof/TC-004/) |
| TC-005 | Hazards now lists each place hazard with its level (Raised / Open) | Pass | ✅✅✅ | — | [proof/TC-005/](proof/TC-005/) |
| TC-006 | Explore cards show the status chip next to the type line; none when the status is null | Pass | ✅✅✅✅ | — | [proof/TC-006/](proof/TC-006/) |
| TC-009 | Offline: Place shows the last cached condition with its 'Updated …' age | Pass | ✅ | — | [proof/TC-009/](proof/TC-009/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._


## Additional observations

## Follow-ups
- TC-009 Place part passes; Explore part fails (D1), owner to confirm AC reading.
- TC-009 Place part passes; Explore part fails (D1), owner to confirm AC reading.
- Emulator screen slept mid-run (first TC-001 attempts Not run); `svc power stayon true` set.
