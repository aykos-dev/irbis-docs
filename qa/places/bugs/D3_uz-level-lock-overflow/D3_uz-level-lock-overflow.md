# D3 · Uzbek level-card lock text runs past the card edge

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 4 - Low |
| Cases | STD-TEXT@place |
| Found | run [2026-10-17_2351](../../runs/2026-10-17_2351/run.md) · build irbis-app 601a6d4 · emulator pixel-8a (font 1.15) |

**Title:** [Place / Level card] - uz "Bu yerga borish uchun 2-darajaga yeting" overflows the card on one line

*Reference: engineering standards STD-TEXT: translated copy must not clip or overflow its container*

**Steps to Reproduce**
1. Guest, language uz, open a place with required level 2 (locked state).
2. Look at the lock line under "yoki undan yuqori".

**Actual:** the lock line extends to and past the right border of the level card; the last word "yeting" touches/overlaps the border. English and Russian fit. · proof: `../../runs/2026-10-17_2351/proof/_run/review/STD-TEXT@place/uz.png`

**Expected:** the lock line wraps inside the card at any locale.

**Cause in code:** `irbis-app/src/features/places/components/LevelCard.tsx:62` — status row (`place.level-locked`) text lacks `flexShrink: 1`/wrapping. Unconfirmed.

## Retests
