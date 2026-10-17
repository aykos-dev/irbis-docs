# D1 · Guest onboarding choices are not merged on sign-up/log-in once any earlier merge happened on the device

| | |
|---|---|
| Status | Closed · not an app defect · retest 2026-10-17 |
| Severity | 3 - Medium |
| Cases | TC-010, TC-011 — the retest re-runs exactly these |
| Found | run [2026-10-17_2045](../../runs/2026-10-17_2045/run.md) · build irbis-app 5299146 · emulator (Android 15) |

**Title:** [Onboarding / Guest merge] - No guest_merge_result after sign-up or log-in; choices never reach the account

*Reference: features/onboarding.md AC7: "guest-merge `onboarding` and saved on the new account" (QA reading, owner to confirm: a guest who signs out and completes onboarding again on the same device should have the new choices merged)*

**Steps to Reproduce**
1. On a device where an earlier sign-up already merged (flag `guest.merged` set), sign out, reset onboarding (`irbis://debug/onboarding/reset`).
2. Complete onboarding with Weekend hiker + Peaks, Lakes; open Profile as guest.
3. Sign up a new QA user (or log in as one).

**Actual:** Sign-up succeeds (`signed_up`), but no `guest_merge_result` / `guest_merged` event is logged; DB row has experience=null, interests={}. Log-in (TC-011) likewise logs no `guest_merge_result` (`locale_applied {ru}` is logged). · proof: `../../runs/2026-10-17_2045/proof/TC-010/1_account.png`, `../../runs/2026-10-17_2045/proof/TC-010/events.txt`

**Expected:** After sign-up the merge request is sent with the onboarding choices, `guest_merge_result` is logged and the account has experience=weekend, interests={peaks,lakes}.

**Cause in code:** `irbis-app/src/shared/contexts/auth.tsx:119` — `mergeGuestData` returns early when `guestMergeDone()` (`guest.merged`, `src/shared/guest/guestStore.ts:28`) is set; it is never cleared on sign-out or onboarding reset (likely cause; the alternative, a swallowed merge error at auth.tsx:129, also logs nothing — not distinguished on device).

## Retests
- 2026-10-17 · run [2026-10-17_2050](../../runs/2026-10-17_2050/run.md) · app 421295e · TC-010, TC-011 Pass. Resolution: not an app defect — QA reset didn't clear guest.merged; fixed in the debug reset link (app 421295e).
