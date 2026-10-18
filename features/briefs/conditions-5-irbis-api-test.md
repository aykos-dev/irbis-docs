# Brief conditions-5-irbis-api-test — expired override / not-yet-started closure are ignored (AC3)

- Spec: features/conditions.md · AC3 · Repo / branch: irbis-api · `feat/conditions` · Depends on: 2e52ef3

## Files
- Touch: `test/conditions.e2e-spec.ts` (add cases only — do not change existing ones)
- Read: `src/features/conditions/conditions.repository.ts` (active filters ~line 134), `admin-conditions.service.ts`

## Behaviour (AC3) — add tests; fix code only if a test fails
- An override whose `expiresAt` is in the past (set directly in the test DB after creating it) is ignored by
  `recomputePlace`: status falls back to closure / season / rules.
- A closure with `startsAt` in the future does not make the place `not_now`; one whose `endsAt` has passed doesn't either.

## Approved packages
none

## Done when
- [ ] 2–3 e2e cases green, `npm run check` green, committed on `feat/conditions`
