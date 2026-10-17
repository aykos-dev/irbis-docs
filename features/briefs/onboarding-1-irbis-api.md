# Brief onboarding-1-irbis-api — onboarding fields + account-wins guest merge

- Spec: features/onboarding.md · ACs in this slice: AC7, AC8 (API side)
- Repo / branch: irbis-api · `feat/onboarding` (create from main)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` (+ NEW migration `onboarding_profile`; never edit old ones) ·
  `src/features/auth/guest-merge/` (new `onboarding-merge.handler.ts`; edit `locale-merge.handler.ts`) ·
  the guest-merge DTO (replace the free-form `onboarding` object with a typed nested DTO) ·
  `MeResponseDto` + `me.service.ts` / `auth.repository.ts` (return + update the new fields) · `openapi.json`.
- Read for patterns (don't change): `locale-merge.handler.ts`, `guest-merge.registry.ts`, `guest-merge.service.ts`,
  `test/auth-recovery.e2e-spec.ts` (guest-merge block ~line 470), `docs/architecture.md` (Domain, boundaries).
- If boundaries forbid a new `src/features/onboarding/` importing auth's registry, keep the handler next to the
  locale handler in `auth/guest-merge/` (that is what this brief expects).

## Behaviour
- Prisma: `enum Experience { beginner weekend experienced }`, `enum Interest { peaks caves lakes camping trails }`;
  `User.experience Experience?`, `User.interests Interest[] @default([])`. Migration name `onboarding_profile`.
- AC7 — guest-merge body `onboarding?: { experience?: Experience; interests?: Interest[] }`, nested validation:
  unknown enum value, duplicate interest, more than 5 interests or an unknown key inside `onboarding` → 400
  `VALIDATION_FAILED` (existing global pipe). Handler key `onboarding`, idempotent.
- AC8 — fill only empty fields: set `experience` only when the account's is null; set `interests` only when the
  account's array is empty (an empty incoming array changes nothing). Never overwrite existing values.
- AC8 — `locale` is no longer overwritten on merge (the account's locale is set at sign-up). The `locale` key stays
  accepted and validated (unknown locale → 400) but the handler does not write; report it under `skipped`.
- `onboarding` is reported under `merged` when the handler ran (even if nothing was empty to fill).
- `GET /v1/me` adds `experience: Experience | null` and `interests: Interest[]` (swagger enums named `Experience`,
  `Interest` so orval generates named types).

## Existing test changed by owner decision (Q8, 2026-10-17)
`test/auth-recovery.e2e-spec.ts` › "200: merges the app language into the account; unhandled parts are reported as
skipped" asserts the old overwrite (`me.locale` becomes `uz`, `skipped: ['onboarding']`). Rewrite only that test to
the Q8 rule (locale kept `en`, `skipped: ['locale']`, `merged: ['onboarding']`) and name it in your reply. Touch no
other existing test.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| POST | /v1/me/guest-merge | `{ locale?, onboarding?: { experience?, interests? } }` | `{ merged: string[], skipped: string[] }` | VALIDATION_FAILED → 400, 401 |
| GET | /v1/me | — | + `experience`, `interests` | 401 |

## Tests (1–3 per AC, e2e in the existing guest-merge block or a new `test/onboarding.e2e-spec.ts`)
- AC7: sign-up then merge `{onboarding:{experience:'weekend',interests:['peaks','lakes']}}` → `GET /v1/me` shows
  them; invalid enum / duplicate interest → 400 VALIDATION_FAILED.
- AC8: account with experience `beginner` + interests `['caves']` merges different values → unchanged; merge
  `{locale:'ru'}` on an `en` account → still `en`, `skipped` contains `locale`.

## Approved packages
none

## Done when
- [ ] tests above, `npm run check` green, committed on `feat/onboarding` (Conventional Commits)
- [ ] `npm run openapi:export` committed
- [ ] reply ≤10 lines: commit hash, check result tail, the rewritten test's name
