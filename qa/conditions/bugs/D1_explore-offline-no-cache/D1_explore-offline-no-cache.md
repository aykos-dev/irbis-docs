# D1 · Explore shows a connection error offline instead of the cached list with condition chips

| | |
|---|---|
| Status | Open · found 2026-10-18 |
| Severity | 3 - Medium |
| Cases | TC-009 |
| Found | run [2026-10-18_1216](../../runs/2026-10-18_1216/run.md) · build irbis-app 92887f9 · emulator-5554 |

**Title:** [Conditions / Explore] - Offline Explore shows "Can't reach Irbis" instead of cached cards with status chips

*Reference: features/conditions.md AC: "Offline: Place and Explore show the last cached condition with its "Updated …" age" (QA reading: Explore cached list; owner to confirm)*

**Steps to Reproduce**
1. Online: open Explore (list loads), open a place whose condition is Caution.
2. Turn network off (app keeps running); reopen the place by deep link: card shows (passes).
3. Open the Explore tab.

**Actual:** Explore shows "Can't reach Irbis. Check your connection and try again."; no `explore.card.<slug>.status` node. · proof: `../../runs/2026-10-18_1216/proof/TC-009/2_offline_explore.png`

**Expected:** Explore shows the last loaded list with the cached Caution chip on the card.

**Cause in code:** not located

## Retests
