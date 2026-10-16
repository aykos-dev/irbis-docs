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
Numbered, testable. Tests are written from these before implementation.
1. …

### Required UI states (every touched client)
- [ ] Loading
- [ ] Empty
- [ ] Error (message + retry)
- [ ] Offline (app: cached view or clear offline message)
- [ ] Permissions denied (if location/camera/etc.)
- [ ] App: keyboard does not cover inputs; safe areas respected
- [ ] Uses design tokens and `components/ui` primitives only

## Out of scope
- …

## Assumptions
- …

## Open questions
- …
