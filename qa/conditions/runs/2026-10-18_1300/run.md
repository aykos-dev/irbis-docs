# Run 2026-10-18_1300 — conditions
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app f5f59cc
**Backend:** irbis-api feat/conditions, CONDITIONS_JOB_ENABLED=false
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** retest D1
**Blocked reasons:** —
**Plan:** ../../cases/Test_conditions.md

## Results
0 pass / 1 fail / 0 blocked / 0 not run — TC-009 (retest D1: Not fixed). First two attempts errored (nav.tab-explore not found, Not run) before a third completed.

## Defects
conditions/D1 — Not fixed.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| [TC-009](#tc-009) | Offline: Place and Explore show the last cached condition with its 'Updated …' age | Fail | TC-009 · Fail | ❌ 1, 2 | [proof/TC-009/](proof/TC-009/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-009"></a>
### TC-009 · Fail · Offline: Place and Explore show the last cached condition with its 'Updated …' age
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** Offline: Place and Explore show the last cached condition with its 'Updated …' age · [→ Test_conditions.md](../../cases/Test_conditions.md#tc-009--p0--offline-place-and-explore-show-the-last-cached-condition-with-its-updated--age)
**Done:** Guest, onboarding done, location granted + mock Tashkent · Peak PLACE (API-nearest) with a Caution forecast · Explore and the place were opened online once in this session so both are cached → 1. seed + online views → 2. go offline (app stays running), reopen Place → 3. read card, then Explore
**Expected** (source: —):
1. `place.condition` is shown with chip 'Caution' and `place.condition-updated` starts with 'Updated' (age) — UI tree + screenshot; `place.condition-offline` is not shown
2. In Explore (offline) `explore.card.<slug>.status` reads 'Caution' — UI tree + screenshot
**Actual:**
1. ❌ card True, chip 'Caution', updated '' — proof/TC-009/1_offline_place.png
2. ❌ explore chip None — proof/TC-009/2_offline_explore.png
**Conclusion:** Offline Explore (cold start) still shows 'Can't reach Irbis', no explore.card.<slug>.status; also place.condition-updated read empty in this run (card+Caution chip present).


## Additional observations

## Follow-ups
- Place card: `place.condition-updated` read '' on this run (earlier run read 'Updated …'); crop shows card top only. Needs a look by the dev/owner if it recurs.
