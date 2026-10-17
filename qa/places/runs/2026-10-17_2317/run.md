# Run 2026-10-17_2317 — places
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/places bf409c5 devRelease
**Backend:** irbis-api feat/places 46e03e6 local
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** core (P0)
**Blocked reasons:** —
**Plan:** ../../cases/Test_places.md

## Results
12 executed: 11 pass, 1 fail, 0 blocked, 0 not run. Pass: TC-001 TC-004 TC-008 TC-010 TC-011 TC-014 TC-018 TC-019 TC-023 TC-028 TC-029. Fail: TC-016.

## Defects
| ID | Severity | Cases | Summary |
|---|---|---|---|
| [D1](../../bugs/D1_empty-state-blank/D1_empty-state-blank.md) | High | TC-016 | Explore empty state renders blank, no Reset button |

## Follow-ups
- Test-script fixes made during the run (not app defects): open_explore relaunches the app after a permission revoke; TC-016 waits for the count 0 event; TC-014 accepts types as a comma string; TC-023/028/029 match uppercase labels, grouped thousands and split 'or higher' text.
- Spec says QA event types: [peak, lake]; app sends a comma string 'peak,lake' (spec wording, owner to confirm).
- Level card shows 'Level 1 · Wanderer' and 'or higher' on separate lines, uppercase 'REQUIRES'; accepted as matching AC8.
- TC-027 not in core; place.not-found / place.not-found-back testIDs do exist in PlaceScreen.tsx:55-59.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | Seed imports 71 places and is idempotent | Pass | TC-001 · Pass · ✅✅✅ | — | [proof/TC-001/](proof/TC-001/) |
| TC-004 | List without a token: sorted by distance, integer metres, total | Pass | TC-004 · Pass · ✅✅✅ | — | [proof/TC-004/](proof/TC-004/) |
| TC-008 | Place detail without a token: shape, empty season/hazards, viewer | Pass | TC-008 · Pass · ✅✅✅ | — | [proof/TC-008/](proof/TC-008/) |
| TC-010 | Explore tab opens for a guest: map, sheet, count header, sorted cards | Pass | TC-010 · Pass · ✅✅✅ | — | [proof/TC-010/](proof/TC-010/) |
| TC-011 | Tapping a card opens Place and Back returns to Explore | Pass | TC-011 · Pass · ✅✅ | — | [proof/TC-011/](proof/TC-011/) |
| TC-014 | Type filter Peaks + Lakes: chip value, list and map refetch, QA event | Pass | TC-014 · Pass · ✅✅✅ | — | [proof/TC-014/](proof/TC-014/) |
| [TC-016](#tc-016) | No match shows the empty state; Reset filters clears everything | Fail | TC-016 · Fail · ❌❌ | ❌ 1, 2 | [proof/TC-016/](proof/TC-016/) |
| TC-018 | First Explore open asks for location; Allow → device origin | Pass | TC-018 · Pass · ✅✅✅ | — | [proof/TC-018/](proof/TC-018/) |
| TC-019 | Denying location falls back to Tashkent with a banner | Pass | TC-019 · Pass · ✅✅✅ | — | [proof/TC-019/](proof/TC-019/) |
| TC-023 | Place screen content (guest, from Tashkent): all fields, nothing extra | Pass | TC-023 · Pass · ✅✅✅ | — | [proof/TC-023/](proof/TC-023/) |
| TC-028 | Level card: qualifies (required level 1) | Pass | TC-028 · Pass · ✅✅✅ | — | [proof/TC-028/](proof/TC-028/) |
| TC-029 | Level card: locked (required level 2 → 'Reach Level 2 to go here') | Pass | TC-029 · Pass · ✅✅✅ | — | [proof/TC-029/](proof/TC-029/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-016"></a>
### TC-016 · Fail · No match shows the empty state; Reset filters clears everything
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** No match shows the empty state; Reset filters clears everything · [→ Test_places.md](../../cases/Test_places.md#tc-016--p0--no-match-shows-the-empty-state-reset-filters-clears-everything)
**Done:** Guest, location granted + mock at Tashkent centre · Explore loaded · A filter combination that the API says has 0 places (picked at run time) → 1. apply cave + difficulty 5-5 → 2. Reset filters
**Expected** (source: —):
1. explore.empty shows with the text 'No places match these filters' and the 'Reset filters' button; QA event explore_filters_applied count 0 — UI tree + screenshot + QA event
2. After Reset: explore.empty is gone, header back to 71, Type / Difficulty / Distance chips show no value (defaults) — UI tree + screenshot
**Actual:**
1. ❌ empty shown True, event {'types': 'cave', 'difficultyMin': 5, 'difficultyMax': 5, 'maxKm': None, 'count': 0} — proof/TC-016/1_empty.png
2. ❌ header None, chips ['Caves', 'Difficulty 5–5', 'Distance'] — proof/TC-016/2_reset.png
**Conclusion:** Empty state: explore.empty is rendered with no children (no title, mascot or Reset filters button); the sheet is blank, so Reset cannot be tapped (header stays at the filtered state).


## Additional observations

## Follow-ups
