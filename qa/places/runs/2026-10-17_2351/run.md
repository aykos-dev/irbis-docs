# Run 2026-10-17_2351 — places
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/places 601a6d4
**Backend:** irbis-api feat/places 46e03e6
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** full
**Blocked reasons:** TC-022 (stale last-known fix with the mock session; no real no-fix state)
**Plan:** ../../cases/Test_places.md

## Results
36 executed: 32 pass, 2 fail (TC-027, STD-TEXT@place), 1 blocked (TC-022), 1 not run (TC-012, pins need eyes). Run 1 of the day was discarded (mock session not up).

## Defects
D2 not-found Back does nothing after a cold deep link (TC-027); D3 uz level-card lock text overflows card (STD-TEXT@place).

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| STD-DARK@explore | Dark mode uses the night tokens — explore | Pass | STD-DARK@explore · Pass | ❌ 1 | [proof/STD-DARK@explore/](proof/STD-DARK@explore/) |
| STD-DARK@place | Dark mode uses the night tokens — place | Pass | STD-DARK@place · Pass | — | [proof/STD-DARK@place/](proof/STD-DARK@place/) |
| STD-OFFLINE@explore | Offline shows a persistent banner and keeps the screen — explore | Pass | STD-OFFLINE@explore · Pass | — | [proof/STD-OFFLINE@explore/](proof/STD-OFFLINE@explore/) |
| STD-OFFLINE@place | Offline shows a persistent banner and keeps the screen — place | Pass | STD-OFFLINE@place · Pass | — | [proof/STD-OFFLINE@place/](proof/STD-OFFLINE@place/) |
| STD-TEXT@explore | Copy is translated — explore | Pass | STD-TEXT@explore · Pass | ❌ 1 | [proof/STD-TEXT@explore/](proof/STD-TEXT@explore/) |
| [STD-TEXT@place](#std-text@place) | Copy is translated — place | Fail | STD-TEXT@place · Fail | ❌ 1 | [proof/STD-TEXT@place/](proof/STD-TEXT@place/) |
| TC-001 | Seed imports 71 places and is idempotent | Pass | TC-001 · Pass | — | [proof/TC-001/](proof/TC-001/) |
| TC-002 | Seed name cleaning and slug rules | Pass | TC-002 · Pass | — | [proof/TC-002/](proof/TC-002/) |
| TC-003 | Seed difficulty and required level bands (boundary elevations) | Pass | TC-003 · Pass | — | [proof/TC-003/](proof/TC-003/) |
| TC-004 | List without a token: sorted by distance, integer metres, total | Pass | TC-004 · Pass | — | [proof/TC-004/](proof/TC-004/) |
| TC-005 | List filters combine with AND (types, difficulty, distance incl. boundaries) | Pass | TC-005 · Pass | — | [proof/TC-005/](proof/TC-005/) |
| TC-006 | List validation: 400 VALIDATION_FAILED matrix with boundary values | Pass | TC-006 · Pass | — | [proof/TC-006/](proof/TC-006/) |
| TC-007 | List pagination by cursor covers every place once | Pass | TC-007 · Pass | — | [proof/TC-007/](proof/TC-007/) |
| TC-008 | Place detail without a token: shape, empty season/hazards, viewer | Pass | TC-008 · Pass | — | [proof/TC-008/](proof/TC-008/) |
| TC-009 | Place detail errors and signed-in viewer | Pass | TC-009 · Pass | — | [proof/TC-009/](proof/TC-009/) |
| TC-010 | Explore tab opens for a guest: map, sheet, count header, sorted cards | Pass | TC-010 · Pass | — | [proof/TC-010/](proof/TC-010/) |
| TC-011 | Tapping a card opens Place and Back returns to Explore | Pass | TC-011 · Pass | — | [proof/TC-011/](proof/TC-011/) |
| [TC-012](#tc-012) | Map pins: type colours, clusters with count, single-pin tap | Not run | TC-012 · Not run | Pins are not in the UI tree. Default zoom shows cluster '6' (step 1 plausible) but Caves-only map shows no pins in the viewport (caves 80/102 km away, camera not fitted) and no pin could be tapped; owner to check pin colour/icon and tap manually. | [proof/TC-012/](proof/TC-012/) |
| TC-013 | Distance format: one decimal under 10 km, whole km from 10 km | Pass | TC-013 · Pass | — | [proof/TC-013/](proof/TC-013/) |
| TC-014 | Type filter Peaks + Lakes: chip value, list and map refetch, QA event | Pass | TC-014 · Pass | — | [proof/TC-014/](proof/TC-014/) |
| TC-015 | Difficulty range 1–3 and distance chips (≤ 50 / ≤ 100 / ≤ 150 / Any) | Pass | TC-015 · Pass | — | [proof/TC-015/](proof/TC-015/) |
| TC-016 | No match shows the empty state; Reset filters clears everything | Pass | TC-016 · Pass | — | [proof/TC-016/](proof/TC-016/) |
| TC-017 | Filters last for the session (tab switch, Place and Back) but not across a restart | Pass | TC-017 · Pass | — | [proof/TC-017/](proof/TC-017/) |
| TC-018 | First Explore open asks for location; Allow → device origin | Pass | TC-018 · Pass | — | [proof/TC-018/](proof/TC-018/) |
| TC-019 | Denying location falls back to Tashkent with a banner | Pass | TC-019 · Pass | — | [proof/TC-019/](proof/TC-019/) |
| TC-020 | 'Turn on' after one denial re-asks; after a second denial it opens app settings; granting there switches to device origin | Pass | TC-020 · Pass | — | [proof/TC-020/](proof/TC-020/) |
| TC-021 | Location switched off on the device falls back to Tashkent | Pass | TC-021 · Pass | — | [proof/TC-021/](proof/TC-021/) |
| [TC-022](#tc-022) | Permission granted but no fix: Tashkent fallback within 10 s | Blocked | TC-022 · Blocked | — | [proof/TC-022/](proof/TC-022/) |
| TC-023 | Place screen content (guest, from Tashkent): all fields, nothing extra | Pass | TC-023 · Pass | — | [proof/TC-023/](proof/TC-023/) |
| TC-024 | Place distance label 'From you' with the device origin | Pass | TC-024 · Pass | — | [proof/TC-024/](proof/TC-024/) |
| TC-025 | Season bar, hazards list and region line when set | Pass | TC-025 · Pass | — | [proof/TC-025/](proof/TC-025/) |
| TC-026 | Locale fallback: Uzbek name and description shown in Russian | Pass | TC-026 · Pass | — | [proof/TC-026/](proof/TC-026/) |
| [TC-027](#tc-027) | Deep link irbis://place/<id> opens Place from a cold start; an unknown id is handled | Fail | TC-027 · Fail · ✅✅❌ | ❌ 3 | [proof/TC-027/](proof/TC-027/) |
| TC-028 | Level card: qualifies (required level 1) | Pass | TC-028 · Pass | — | [proof/TC-028/](proof/TC-028/) |
| TC-029 | Level card: locked (required level 2 → 'Reach Level 2 to go here') | Pass | TC-029 · Pass | — | [proof/TC-029/](proof/TC-029/) |
| TC-030 | Level names 1–7 and the qualify boundary (level 1 vs 2) | Pass | TC-030 · Pass | — | [proof/TC-030/](proof/TC-030/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="std-text@place"></a>
### STD-TEXT@place · Fail · Copy is translated — place
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated — place · [→ Test_places.md](../../cases/Test_places.md#std-textplace--p2--copy-is-translated)
**Done:** 1. ru — open the screen → 2. uz — open the screen
**Expected** (source: —):
1. No English catalog string left on screen in Russian or Uzbek — UI tree
**Actual:**
1. ❌ untranslated: {'ru': ['Уровень 2 · Землекоп'], 'uz': ['2-daraja · Qazuvchi']} — no proof
**Conclusion:** uz crop: lock line 'Bu yerga borish uchun 2-daraja...' runs past the right edge of the level card (clipped at border). ru fine; script flagged strings were false positives.

<a id="tc-012"></a>
### TC-012 · Not run · Map pins: type colours, clusters with count, single-pin tap
**Group:** Variants · **Priority:** P1 · **Env:** Android · auto (adb)
**Case:** Map pins: type colours, clusters with count, single-pin tap · [→ Test_places.md](../../cases/Test_places.md#tc-012--p1--map-pins-type-colours-clusters-with-count-single-pin-tap)
**Reason:** Pins are not in the UI tree. Default zoom shows cluster '6' (step 1 plausible) but Caves-only map shows no pins in the viewport (caves 80/102 km away, camera not fitted) and no pin could be tapped; owner to check pin colour/icon and tap manually.
**Proof:** proof/TC-012/1_map_default.png, proof/TC-012/2_map_caves.png, proof/TC-012/3_after_pin_tap.png, proof/TC-012/__pycache__, proof/TC-012/case.py, proof/TC-012/events.txt, proof/TC-012/video_steps.tsv

<a id="tc-022"></a>
### TC-022 · Blocked · Permission granted but no fix: Tashkent fallback within 10 s
**Group:** Variants · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Permission granted but no fix: Tashkent fallback within 10 s · [→ Test_places.md](../../cases/Test_places.md#tc-022--p2--permission-granted-but-no-fix-tashkent-fallback-within-10-s)
**Reason:** —
**Proof:** proof/TC-022/2_fallback.png, proof/TC-022/__pycache__, proof/TC-022/case.py, proof/TC-022/events.txt, proof/TC-022/video_steps.tsv

<a id="tc-027"></a>
### TC-027 · Fail · Deep link irbis://place/<id> opens Place from a cold start; an unknown id is handled
**Group:** Variants · **Priority:** P1 · **Env:** Android · auto (adb)
**Case:** Deep link irbis://place/<id> opens Place from a cold start; an unknown id is handled · [→ Test_places.md](../../cases/Test_places.md#tc-027--p1--deep-link-irbisplaceid-opens-place-from-a-cold-start-an-unknown-id-is-handled)
**Done:** Guest, onboarding done · App force-stopped → 1. cold deep link → 2. unknown id → 3. Back
**Expected** (source: —):
1. The seeded place opens with place.name equal to its name_uz and QA event place_viewed {slug} — UI tree + QA event
2. The unknown id shows place.not-found with the text 'This place isn't available' (ru 'Это место недоступно', uz 'Bu joy mavjud emas') and a back button (place.not-found-back); no place.name, no crash — UI tree + screenshot
3. Back leaves the error state to a tab screen without a crash — UI tree
**Actual:**
1. ✅ name "Bo'ritog'", event {'slug': 'boritog-1295', 'requiredLevel': 1, 'qualifies': True} — proof/TC-027/1_link.png
2. ✅ state 'place.not-found', text True — proof/TC-027/2_notfound.png
3. ❌ tab bar visible, no crash — no proof
**Conclusion:** Step 3: after a cold deep link to an unknown id, tapping place.not-found-back leaves the not-found screen unchanged (goBack with empty stack is a no-op); no tab bar. Re-checked with a standalone cold link.


## Additional observations

## Follow-ups
- Owner: TC-012 pins (colour/icon, tap) by hand; Caves-only map showed no pins in the viewport at the default camera.
- Owner: TC-022 no-fix fallback without the mock session. Dark: map tiles stay light (design call).
- Script fixes during the run: TC-019/020 open_explore, TC-020 resume app, TC-024 open from card + uppercase label, TC-030 name format, apply_filters sheet-gone wait.
