# D3 · Changing the system font size mid-onboarding restarts the flow at Meet Irbis

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 4 - Low |
| Cases | STD-TEXT@language — the retest re-runs it (and the other STD-TEXT@ screens once D2 is fixed) |
| Found | run [2026-10-17_2052](../../runs/2026-10-17_2052/run.md) · build irbis-app 421295e · emulator (Android 15) |

**Title:** [Onboarding / Flow] - A font-scale change on a step drops the user back to Meet Irbis

**Steps to Reproduce**
1. Guest, first run, walk Meet Irbis -> Get started (Language step).
2. `adb shell settings put system font_scale 2.0`.

**Actual:** the activity is recreated and the app shows Meet Irbis again; the Language step and any choices on screen are lost. (A signed-in device goes to the tabs, by design.) · proof: `../../runs/2026-10-17_2052/proof/_run/review/STD-TEXT@language/en_font2.0.png`

**Expected:** (QA reading, owner to confirm) the current step survives a configuration change.

**Cause in code:** not located (root/onboarding navigator state is rebuilt on recreate; `OnboardingNavigator.tsx` always starts at `Splash`)

## Retests
