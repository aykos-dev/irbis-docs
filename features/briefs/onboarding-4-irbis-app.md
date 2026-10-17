# Brief onboarding-4-irbis-app — choices into the account; account language wins on log-in

- Spec: features/onboarding.md · ACs in this slice: AC7, AC8 (app side)
- Repo / branch: irbis-app · `feat/onboarding`
- Depends on: onboarding-1-irbis-api (api `feat/onboarding`, `openapi.json` exported) and onboarding-3-irbis-app

## Files
- Touch: `src/features/onboarding/onboardingStore.ts` (register a guest item) · `src/shared/contexts/auth.tsx`
  (`startSession` / `mergeGuestData`: apply the account locale after log-in) · `src/shared/api/generated/` via
  `npm run gen:api` only.
- Read for patterns: `src/shared/guest/guestStore.ts` (`registerGuestItem`, `collectGuestData`, the pre-registered
  `language` item), existing auth tests for `mergeGuestData` / `startSession`, `src/shared/i18n/index.ts`.

## Behaviour
- First run `npm run gen:api` (api spec path as configured in orval). Use the generated `Experience`, `Interest`,
  `GuestMergeDto`, `MeResponseDto` types; never hand-write them.
- AC7 — register guest item `onboarding` whose `collect()` returns `{ onboarding: { experience, interests } }` from
  MMKV (`onboarding.experience`, `onboarding.interests`), omitting keys that are unset/empty; returns `undefined` when
  both are unset (✕ path). Validate stored values against the generated enums; drop anything unknown.
- Sign-up and log-in both run the existing once-per-device merge; the API decides fill-if-empty (AC8), so the client
  sends the same payload in both cases.
- AC8 — after a successful log-in (not sign-up), once `GET /v1/me` is loaded, call `setLocale(me.locale)` if it
  differs from the current app locale. Sign-up keeps the device language (it was sent at sign-up).
- Keep the existing `language` guest item as is (the API now reports `locale` under `skipped`).
- Do not clear `onboarding.experience` / `onboarding.interests` after merge (local copy for future features).

## API (generated hooks only)
| Method | Path | Request | Response | Errors |
|---|---|---|---|---|
| POST | /v1/me/guest-merge (`useMeGuestMerge`) | `{ locale?, onboarding?: { experience?, interests? } }` | `{ merged, skipped }` | VALIDATION_FAILED 400 |
| GET | /v1/me (`useMeGet`) | — | + `experience`, `interests` | 401 |

## Copy
none new.

## testIDs · QA events
existing `guest_merged { keys }` must list `onboarding` when it was sent; add `locale_applied { locale }` when the
account language is applied after log-in.

## Approved packages
none

## Done when
- [ ] tests: collect() payload (set / ✕ unset / unknown value dropped); log-in applies `me.locale`, sign-up does not
- [ ] `npm run check` green, committed (generated files in their own commit is fine); reply ≤10 lines
