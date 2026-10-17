# D2 · Place not-found screen: Back does nothing after a cold deep link

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 3 - Medium |
| Cases | TC-027 |
| Found | run [2026-10-17_2351](../../runs/2026-10-17_2351/run.md) · build irbis-app 601a6d4 · emulator pixel-8a |

**Title:** [Place / Deep link] - Back on the "This place isn't available" screen leaves the user stuck

*Reference: features/places.md (deep link): "unknown place id (deep link) → empty state "This place isn't available" + back"*

**Steps to Reproduce**
1. Force-stop the app.
2. Open `irbis://place/00000000-0000-4000-8000-000000000000`.
3. Tap Back (`place.not-found-back`).

**Actual:** the not-found screen stays; no tab bar appears (`nav.tab-explore` absent). Same with the top-left back arrow. The Place screen is the only route in the stack, so `navigation.goBack()` is a no-op. Reproduced twice (TC-027 and a standalone cold link). · proof: `../../runs/2026-10-17_2351/proof/TC-027/2_notfound.png`

**Expected:** Back leaves the error state to the tab screen (Explore or home), never a dead end.

**Cause in code:** `irbis-app/src/features/places/screens/PlaceScreen.tsx:47` — `const goBack = () => navigation.goBack();` with no `canGoBack()` fallback to `MainTabs`.

## Retests
