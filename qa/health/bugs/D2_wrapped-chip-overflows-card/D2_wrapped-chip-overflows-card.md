# D2 · Status chip runs past the card when its label wraps

| | |
|---|---|
| Status | Open · reproduced 2026-10-17 |
| Severity | 3 - Medium |
| Feature | [features/health.md](../../../../features/health.md) |
| Found | run [2026-10-17_0117](../../runs/2026-10-17_0117/run.md), TC-006, TC-007, TC-009 |
| Build | uz.irbis.app.dev 0.0.1 devRelease arm64, irbis-app commit 2141d96; irbis-api 8fb74fa |
| Video | [D2_wrapped-chip-overflows-card.mp4](video/D2_wrapped-chip-overflows-card.mp4) (step captions under the screen) |

## Bug

**Title:** [Status / Status chip] - Chip runs past the card's right border when its label wraps to two lines

**Description**

On the Status screen, a status chip whose label wraps to two lines grows wider than the card and its right end sticks
out past the card's border. It happens in Russian ("База данных работает") and Uzbek ("Ma'lumotlar bazasi ishlayapti")
at the phone's normal font size (1.15 on the test phone), and in English at larger font sizes. The shared `StatusChip`
is used for every condition status in the app, so the same overflow will appear wherever a long label is shown.

*Reference: irbis-app engineering standards §13: "Layouts tolerate +40% string length. Buttons grow or wrap; they don't truncate." and §12: "layouts wrap or scroll, never clip" (features/health.md AC4: "Copy is in uz / ru / en via i18n keys").*

- **Environment / Build Version:** Galaxy S25 Ultra (Android 16), font size 1.15, Irbis app 0.0.1 dev release, local API 0.0.1

**Steps to Reproduce**

1. Set the phone's font size to the next step above default (1.15) and the app language to Russian.
2. Open the app on the Status screen with the API and database running.
3. Look at the "База данных работает" chip against the card's right border.

**Actual Result**

The chip label wraps to two lines and the green chip extends past the card's right border.

**Expected Result**

The chip stays inside the card: the label wraps within the chip and the chip's width never exceeds the card's content area.

---

## Internal notes

### Recording
- Re-record: `~/.claude/venvs/qa/bin/python others/repro.py` (retest: `… repro.py retest-YYYY-MM-DD`)
- Video: [video/D2_wrapped-chip-overflows-card.mp4](video/D2_wrapped-chip-overflows-card.mp4)

| Video time | Caption |
|---|---|
| 00:00 | Setup: API and database running; phone font size 1.15 |
| 00:01 | Step 1: Set the app language to Russian |
| 00:01 | Step 2: Open the app |
| 00:05 | Observed: the database chip label wraps to two lines |
| 00:09 | Expected / Result: FAIL |

Screenshot: [image/01_ru_status.png](image/01_ru_status.png). Also seen in run proof `TC-007/1_uz.png` (Uzbek) and
`TC-009/1_font2.png` (English, font 2.0).
Note: the uiautomator bounds of `health.db-chip` stay inside the card — the overflow is in the drawn chip, so the
screenshot is the proof, not the node bounds.

### Which AC is broken
- AC4 + standards §12/§13 (wrap, never clip; +40% text).
- Cause in code (for the developer): `irbis-app/src/shared/components/StatusChip.tsx:77-85` — the chip row has
  `alignSelf: 'flex-start'` with no `maxWidth: '100%'`, and the label has no `flexShrink: 1`, so a wrapped label sizes
  the chip by its unwrapped text width.

### Why Medium
Visible on the owner's own phone at its normal font size in two of the three app languages, in a shared component that
every condition chip will reuse.
