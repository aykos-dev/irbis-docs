# D1 · Explore empty state renders blank: no text, no Reset filters button

| | |
|---|---|
| Status | Open · found 2026-10-17 |
| Severity | 2 - High |
| Cases | TC-016 |
| Found | run [2026-10-17_2317](../../runs/2026-10-17_2317/run.md) · build irbis-app bf409c5 · emulator pixel-8a |

**Title:** [Explore / Filters] - No-match result shows a blank sheet; empty text and Reset filters button missing

*Reference: features/places.md AC5: "No match → empty state "No places match these filters" with …" (Reset filters button)*

**Steps to Reproduce**
1. Guest, location granted, Explore open with 71 places.
2. Apply Type = Caves and Difficulty 5-5 (API returns total 0 for this combination).

**Actual:** QA event `explore_filters_applied {types: cave, difficultyMin: 5, difficultyMax: 5, count: 0}` fires and `explore.empty` is in the UI tree, but the node has no children: no title "No places match these filters", no mascot, no `explore.filter.reset` button. The sheet is visibly blank, so filters cannot be reset from the empty state. · proof: `../../runs/2026-10-17_2317/proof/TC-016/1_empty.png`, `../../runs/2026-10-17_2317/proof/TC-016/2_reset.png`

**Expected:** `explore.empty` shows "No places match these filters" and a "Reset filters" button (`explore.filter.reset`) that clears all filters.

**Cause in code:** not located. Suspects: `irbis-app/src/features/places/screens/ExploreScreen.tsx:77` EmptyState inside `BottomSheet` (children invisible), or the `FadeIn` entering animation in `src/shared/components/EmptyState.tsx` never completing.

## Retests
