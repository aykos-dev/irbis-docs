---
description: Write the Android test plan (concrete, AC-traced cases) for an approved feature spec
argument-hint: <slug>
---
Write the test plan for: $ARGUMENTS

Inputs: `features/<slug>.md` (must be Approved — if not, stop and say so), the app's
`irbis-app/docs/engineering-standards.md` Quick gate, and `qa/_templates/Test_TEMPLATE.md`.
Output: `qa/<slug>/cases/Test_<slug>.md`. Do not write case scripts here — `/qa-run` does that.

1. **Requirement inventory.** Every numbered AC is a requirement. Also count as requirements: each named
   threshold, state transition, error path, QA event the spec names, and "unchanged" out-of-scope contracts.
2. **Unclear points first.** Walk the spec for anything a test needs that the spec does not state (a value,
   which side of a boundary is inclusive, what happens at empty / offline / midnight / permission denied).
   For each point where *the two readings would give different expected results*, ask me with
   AskUserQuestion before writing: up to 4 per round, max 3 rounds; options are concrete testable behaviours
   (never yes/no), the one the spec best supports first, and "Leave open" last. Never ask what the spec,
   ADRs or code already answer. Record each answer in the spec's **Assumptions** section as
   `Q{n} (owner, YYYY-MM-DD): …`. Points I leave open → **Open questions** in the spec; their cases carry `⚠️ Q{n}`.
3. **Derive cases per requirement** (count comes from the requirements, never a target number):
   - Every requirement gets ≥1 Core case (does the feature honour it at all?).
   - Pushed cases (boundary, broken, absent, raced): Core when the failure blocks release, else Supplementary.
   - Technique sets the count: BVA with real numbers (199 / 200 / 201 m, 23:59:59 / 00:00:00), EP one value
     per class, DT one case per combination with a distinct outcome, ST one per allowed and per forbidden
     transition (one invalid transition per case), EG for the rest.
   - Add the engineering-standards cases for this feature's screens (offline, largest font, dark mode,
     landscape, keyboard, Android back with dirty form, process death, permission denied/blocked) as
     Supplementary unless the spec makes one Core.
   - Forbidden: "repeat TC-x on another platform", cosmetic cases the spec never asked for, two requirements
     in one case.
4. **Test data before cases.** Concrete values (accounts, mock points via `offset()`/`distance_m()` in
   `scripts/qa/rec/drv.py`, spot ids). Unknown values → `⚠️ DATA` with the requirement for the value. Never
   write a phone number unmasked, a token, password or OTP — point to the env var that holds it.
5. **Write the cases** in the template format: exact UI strings in quotes (with locale when it matters),
   testIDs for elements, every Expected bullet with its evidence (`screenshot`, `event log`,
   `screenrecord+frames`, `api: <curl>`, `db: <query>`), a window + trigger for every absence or timing claim.
6. **Coverage matrix**: every AC row has a non-empty Core cell; every TC in exactly one row.

Reply with: case counts (Core / Supplementary), the matrix summary line, answers recorded, open `⚠️ Q`
and `⚠️ DATA` items. Next step: `/qa-run <slug> <build>`.
