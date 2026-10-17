# D1 · irbis:// deep links do not open the app (no Android intent-filter)

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 2 - High |
| Cases | TC-040 |
| Found | run [2026-10-17_1706](../../runs/2026-10-17_1706/run.md) · build irbis-app 1a4978d · emulator-5554 |

**Title:** [Auth / Deep links] - irbis://debug/status is not delivered to the app, Status never opens

*Reference: features/auth.md AC10: "The Status screen (M0) ... is reachable in dev/staging builds through the Debug screen and `irbis://debug/status`"*

**Steps to Reproduce**
1. Cold start the dev build (tab bar shown).
2. `adb shell am start -W -a android.intent.action.VIEW -d irbis://debug/status uz.irbis.app.dev`

**Actual:** adb answers "unable to resolve Intent"; the app stays on the Path tab, `health.status-card` never appears. `irbis://profile` and `irbis://debug` fail the same way. Via Profile → Debug tools → API status the card opens (TC-040 bullet 2 passes). · proof: `../../runs/2026-10-17_1706/proof/TC-040/3_link.png`

**Expected:** `irbis://debug/status` opens `health.status-card`.

**Cause in code:** `irbis-app/android/app/src/main/AndroidManifest.xml:21` — only a MAIN/LAUNCHER intent-filter; no VIEW/BROWSABLE filter for scheme `irbis` (JS linking config in `src/app/navigation/linking.ts` is fine).

## Retests
