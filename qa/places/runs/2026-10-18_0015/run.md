# Run 2026-10-18_0015 — places
**Status:** in progress
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/places feadf6e
**Backend:** irbis-api feat/places 46e03e6
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** retest D2 D3
**Blocked reasons:** —
**Plan:** ../../cases/Test_places.md

## Results
2 pass / 0 fail. TC-027, STD-TEXT@place (script flagged level name as untranslated; crop shows it is translated).
Retest: D2 Fixed, D3 Fixed.

## Defects

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-027 | Deep link irbis://place/<id> opens Place from a cold start; an unknown id is handled | Pass | TC-027 · Pass | — | [proof/TC-027/](proof/TC-027/) |
| STD-TEXT@place | Copy is translated — place | Pass | STD-TEXT@place · script Fail, crop Pass | — | [proof/STD-TEXT@place/](proof/STD-TEXT@place/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

## Additional observations

## Follow-ups
