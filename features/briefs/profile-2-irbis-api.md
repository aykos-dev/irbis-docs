# Brief profile-2-irbis-api — username change, preferences, session-aware revocation

- Spec: features/profile.md · ACs in this slice: AC2, AC6 (server preferences)
- Repo / branch: irbis-api · `feat/profile`
- Depends on: profile-1-irbis-api (schema + profile module on the branch)

## Files
- Touch: `src/features/profile/profile.controller.ts`, `profile.service.ts`, `profile.repository.ts`,
  `dto/profile.request.dto.ts`, `profile.errors.ts`, tests ·
  `src/common/auth-user.ts` (`AuthUser.sessionId?`) · `src/common/guards/jwt-auth.guard.ts` (parse `sid`) ·
  `src/features/auth/guards/account-status.guard.ts` (keep `sessionId` when replacing the role) ·
  `src/features/auth/token.service.ts` (`signAccess({id, role, sessionId})`; `startSession`/`refresh` pass the
  refresh family id) · `src/features/auth/auth.repository.ts`
  (`revokeAllForUserExceptFamily`, `updateUsername` if useful) · `src/features/auth/auth.module.ts`
  (export `AuthRepository`, `PasswordService`, `TokenService` for `ProfileModule`) · `openapi.json`
- Read for patterns: `src/features/auth/auth.service.ts` (password verify + normalize), `username.rules.ts`,
  `auth.errors.ts`, `token.service.ts`, `auth.repository.ts`, `common/errors/validation.error.ts`,
  `common/decorators/throttle.decorator.ts`, `test/levels-api.e2e-spec.ts`.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| PATCH | /v1/me | user, `@Throttled('auth')` | `username?`, `currentPassword?`, `preferences?` + profile fields from slice 1 | `MeResponse` | 400 VALIDATION_FAILED, 401 INVALID_PASSWORD, 403, 409 USERNAME_TAKEN, 429 |

`preferences` (all optional, nested partials): `{ showStats?, showHomeRegion?, units?, appearance?,
notifications?: { streakReminders?, dailyGame?, dailyGameTime?, groupsMessages?, social?, offers? },
privacy?: { publicProfile?, findBuddies? } }`. `tripSafety` and `shareLocation` are not writable.

## Behaviour
- AC2 — If `username` is present and differs after `normalizeUsername`: `currentPassword` is required (400
  `fieldErrors.currentPassword=['required']` when absent) and must verify against `passwordHash` (401
  `INVALID_PASSWORD` when wrong). Validate with the existing `usernameProblem`; reuse `UsernameInvalidError`,
  `UsernameReservedError`, `UsernameTakenError` (409). Same normalized username → no-op, no password check.
  On success update the lowercase username and revoke every refresh-token family for the user **except** the
  caller's `sessionId`; the current session keeps working. Login with the new username works; the old one does
  not.
- Access tokens gain `sid` = the refresh family id. `AuthUser` gets `sessionId?`; the JWT guard reads a string
  `sid`; the account-status guard preserves it when it replaces the role. Old tokens without `sid` are treated
  as having no current family (revoke all on username change) — do not fail authentication for missing `sid`.
- AC6 server side — Apply only the preference keys present. Defaults stay as slice 1. `units` is
  `metric|imperial`, `appearance` is `light|dark|auto`, `dailyGameTime` matches `^([01]\d|2[0-3]):[0-5]\d$`.
  `notifications.tripSafety` and `privacy.shareLocation` are always returned true / `trips` and are rejected or
  ignored by the whitelist; the response always shows them. Return the updated `MeResponse`.
- Password values are never logged or echoed. Keep `currentPassword` out of Swagger examples beyond
  `format: password`.
- Swagger operation id stays `Me_update`; extend the request DTO so orval regenerates `useMeUpdate`.

## Copy
none (API).

## testIDs · QA events
none · none.

## Approved packages
none.

## Done when
- [ ] unit: username normalized; same-name no-op; missing/wrong password errors; invalid/reserved/taken codes;
  preferences partial merge; daily-time regex; immutable tripSafety/shareLocation
- [ ] e2e: two log-ins for one user; change username with the first session → first refresh still works, second
  refresh fails; login with new username works and old username fails; new access token has `sid`; preference
  PATCH persists and `GET /v1/me` reflects it
- [ ] `npm run check` green (output in summary) · `npm run openapi:export` committed · `graphify update .`
