# Run 2026-10-17_0127 — health
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — devRelease arm64 APK, irbis-app 10701d9 (fix/health-d2)
**Backend:** local irbis-api 8fb74fa via adb reverse
**Device:** SM-S938B (Android 16)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** retest of health/D2: TC-006, TC-007, TC-009; re-run of 2026-10-17_0117
**Blocked reasons:** —
**Plan:** ../../cases/Test_health.md

## Results
**Pass 3** (TC-006, TC-007, TC-009) · Fail 0 · Blocked 0 · Not run 0. Confirms health/D2 fixed on 10701d9.

## Defects
None new. health/D2 → Fixed (see its bug file).

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| [TC-006](#tc-006) | Russian copy | Pass | Russian copy complete; wrapped DB chip now inside the card | — | [proof/TC-006/](proof/TC-006/) |
| [TC-007](#tc-007) | Uzbek copy | Pass | Uzbek copy complete; wrapped chip inside the card | — | [proof/TC-007/](proof/TC-007/) |
| [TC-009](#tc-009) | Largest font size does not clip the card | Pass | font 2.0: texts wrap, 'Database is up' chip inside the card | — | [proof/TC-009/](proof/TC-009/) |

## Cases

<a id="tc-006"></a>
### TC-006 · Pass · Russian copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Russian copy · [→ Test_health.md](../../cases/Test_health.md#tc-006--p2--russian-copy)
**Done:** API-UP → 1. Set the app language to Russian and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Russian, matching `src/shared/i18n/ru` — no English left — screenshot
2. Layout does not clip or truncate any Russian label — screenshot
**Actual:**
1. ✅ Статус, API работает, База данных работает, Проверено в 01:27 — no English UI copy — proof/TC-006/1_ru.png
2. ✅ health.db-chip wraps to 2 lines and ends inside the card border — proof/TC-006/1_ru.png
**Conclusion:** D2 fixed for Russian at font 1.15. (Script flagged 'Окружение: dev' — env value; check fixed in the library script.)

<a id="tc-007"></a>
### TC-007 · Pass · Uzbek copy
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Uzbek copy · [→ Test_health.md](../../cases/Test_health.md#tc-007--p2--uzbek-copy)
**Done:** API-UP → 1. Set the app language to Uzbek and cold start
**Expected** (source: AC4):
1. Every text on the Status screen is Uzbek (Latin), matching `src/shared/i18n/uz` — screenshot
**Actual:**
1. ✅ English texts left: []; all: ['IRBIS', 'Holat', 'API ishlayapti', 'Ma’lumotlar bazasi ishlayapti', 'v0.0.1', '01:27 da tekshirildi', 'Muhit: dev', '01:27'] — proof/TC-007/1_uz.png
**Conclusion:** D2 fixed for Uzbek.

<a id="tc-009"></a>
### TC-009 · Pass · Largest font size does not clip the card
**Group:** Supplementary · **Priority:** P3 · **Env:** Android · auto (adb) · resources: API-UP
**Case:** Largest font size does not clip the card · [→ Test_health.md](../../cases/Test_health.md#tc-009--p3--largest-font-size-does-not-clip-the-card)
**Done:** API-UP → 1. Font scale 2.0, cold start
**Expected** (source: standards §12):
1. All card texts fully visible (wrap or scroll, no clipped words), Retry/refresh still reachable — screenshot
**Actual:**
1. ✅ all card texts readable and wrapped; health.db-chip ends inside the card border — proof/TC-009/1_font2.png
**Conclusion:** D2 fixed at the largest font.


## Additional observations

## Follow-ups
