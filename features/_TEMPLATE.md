# <slug>

- Status: Draft | Approved | Done
- Surfaces: api | web | app
- Related ADRs:

## Goal
One or two sentences of user-visible behaviour.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|

## Data model changes
Prisma models/fields added or changed. New migration name.

## Acceptance criteria
Numbered `AC1`, `AC2` … and never renumbered once approved (tests, QA cases and bug reports quote them).
Each is testable and states concrete values (200 m, once per UTC day, +50 XP), not "nearby" or "quickly".
Unit/e2e tests and the QA plan (`qa/<slug>/cases/`) are written from these.
- **AC1** — …

### QA events (app, dev/staging builds)
Events the app logs via `qaLog` so QA can prove invisible results: `name { props }` — no personal data.
- `…`

### testIDs (app)
Elements QA scripts tap or assert on: `<slug>.<element>` (e.g. `spot.checkin-button`).

### Required UI states (every touched client)
Full list: each repo's `docs/engineering-standards.md` Quick gate. Waivers go in a "Waivers" section below.
- [ ] Loading
- [ ] Empty
- [ ] Error (message + retry)
- [ ] Offline (app: cached view or clear offline message)
- [ ] Permissions denied (if location/camera/etc.)
- [ ] App: keyboard does not cover inputs; safe areas respected; haptics; press states
- [ ] Uses design tokens and `src/shared/components` primitives only

## Waivers
- none

## Out of scope
- …

## Assumptions
- Q1 (owner, YYYY-MM-DD): …

## Open questions
- …
