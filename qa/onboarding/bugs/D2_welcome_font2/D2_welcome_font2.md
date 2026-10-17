# D2 · Meet Irbis at font scale 2.0: Get started and I already have an account are pushed off-screen and unreachable

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 2 - High |
| Cases | STD-TEXT@welcome (also unblocks STD-TEXT@language/experience/interests/companion en@2.0) — the retest re-runs exactly these |
| Found | run [2026-10-17_2052](../../runs/2026-10-17_2052/run.md) · build irbis-app 421295e · emulator (Android 15) |

**Title:** [Onboarding / Meet Irbis] - At largest font the CTAs fall off-screen and the screen does not scroll

*Reference: irbis-app docs/engineering-standards.md (layout survives font scale 2.0); features/onboarding.md AC1 (Meet Irbis offers Get started / I already have an account)* (QA reading, owner to confirm the standard's wording)

**Steps to Reproduce**
1. Set system font scale 2.0 (`adb shell settings put system font_scale 2.0`), language English.
2. `irbis://debug/onboarding/reset`, wait for Meet Irbis.
3. Look for `onboarding.get-started`; swipe up.

**Actual:** the mascot bubble and headline fill the screen; `onboarding.get-started` and `onboarding.have-account` are not in the UI tree and a swipe up does not reveal them, so a user with the largest font cannot start onboarding or log in. At 1.15 and in ru/uz it fits. · proof: `../../runs/2026-10-17_2052/proof/_run/review/STD-TEXT@welcome/en_font2.0.png`

**Expected:** at font 2.0 both buttons are reachable (content scrolls or shrinks).

**Cause in code:** not located (Welcome screen layout under `irbis-app/src/features/onboarding/`: fixed non-scrolling column)

## Retests
