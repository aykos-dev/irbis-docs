# auth

- Status: Draft — decisions taken 2026-10-17; remaining questions asked at `/feature auth` step 1
- Surfaces: api | app (web admin log-in reuses the API; its screen is built with the first web feature)
- Related ADRs: ADR-001 (auth), ADR-003 (API style)
- Requirements: Product Overview § Accounts & sign-in · Screens: `design/canvas/AccLogin`, `AccSignup`, `AccGate`,
  `AccForgot`, `AccReset`, `AccGuestProfile`, `Onb1Welcome` ("I already have an account")

## Goal
Anyone can explore Irbis without an account. When they do something that saves or earns, the app asks them to log in
or create an account (username + password), keeps what they did as a guest, and lets them reset a forgotten password
with an SMS code if they added a recovery phone.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | /v1/auth/sign-up | public | username, password, recoveryPhone?, locale, acceptTerms | tokens + me | USERNAME_TAKEN, USERNAME_INVALID, PASSWORD_WEAK, VALIDATION_FAILED |
| GET | /v1/auth/username-available?u= | public | — | { available } | RATE_LIMITED |
| POST | /v1/auth/log-in | public | username, password | tokens + me | INVALID_CREDENTIALS, ACCOUNT_LOCKED, RATE_LIMITED |
| POST | /v1/auth/refresh | refresh token | — | tokens | REFRESH_REUSED, REFRESH_EXPIRED |
| POST | /v1/auth/sign-out | user | — | 204 | — |
| POST | /v1/auth/password/forgot | public | username | 202 (same response whether or not the account/phone exists) | RATE_LIMITED |
| POST | /v1/auth/password/reset | public | username, code, newPassword | tokens + me | CODE_INVALID, CODE_EXPIRED, CODE_ATTEMPTS, PASSWORD_WEAK |
| PUT / POST | /v1/me/recovery-phone · /verify | user | phone · code | me | PHONE_INVALID, CODE_INVALID |
| POST | /v1/me/guest-merge | user | onboarding choices, lesson attempts, saved places (device ids) | merged summary | VALIDATION_FAILED |

## Data model changes
`User` gains `username` (unique, case-insensitive), `passwordHash`, `recoveryPhone?` (encrypted),
`recoveryPhoneVerifiedAt?`; new `PasswordReset`, `LoginAttempt`; `RefreshToken` (ADR-001). Migration `auth_init`.

## Acceptance criteria
- **AC1** — A new user can complete onboarding and use Path, Explore, Lessons, Community (read) and Profile without an
  account; no screen blocks on log-in. SOS and Safety center work with no account.
- **AC2** — Actions that save or earn (check in, start a trip plan, finish a lesson for XP, earn a badge, post, like,
  comment, join a group, online game) open the log-in prompt sheet (A3) for a guest instead of performing the action.
  "Not now" closes the sheet and leaves the user on the same screen with nothing lost.
- **AC3** — After sign-up or log-in from the sheet, the interrupted action resumes once without re-tapping.
- **AC4** — Sign-up takes username + password (+ optional recovery phone, + terms checkbox) and logs the user in.
  Username availability shows while typing (pristine → validating → success / error).
- **AC5** — Guest data (onboarding choices, completed lessons, saved places) is merged into the account on the first
  sign-up or log-in; XP for merged lessons is awarded under the normal daily caps; merge runs once.
- **AC6** — Log-in with a wrong username or password shows one generic error ("Username or password is wrong") — never
  which one; repeated failures are rate-limited / locked per the values in Assumptions.
- **AC7** — Forgot password: entering a username sends a 6-digit SMS code to the recovery phone if one exists; the
  screen response is identical either way. A correct code + new password logs the user in and signs out every other
  session. Codes are single-use, expire, and lock after too many attempts.
- **AC8** — Accounts without a recovery phone see the support path on A4; Settings nudges them to add a phone.
- **AC9** — Sign-out clears tokens from the Keychain and returns to the guest state (not to a log-in wall).
- **AC10** — A Profile tab for a guest shows A6 (Create free account / Log in / Language / Safety & SOS).
- **AC11** — Tokens: access ~15 min, refresh rotated on every use; reuse of an old refresh token revokes the family.

### Required UI states (every touched client)
- [ ] Loading (submit buttons pending, availability check spinner)
- [ ] Error (field errors under fields; generic credential error; network error with retry)
- [ ] Offline (sign-up / log-in / reset refused with a clear message; guest browsing of cached data continues)
- [ ] App: keyboard never covers inputs; `returnKeyType` chain; password show/hide; `textContentType` /
      `autoComplete` username / password / new-password / one-time-code / tel
- [ ] Uses design tokens and `src/shared/components` primitives only

### QA events (app, dev/staging builds)
- `auth_gate_shown { reason }` · `auth_gate_dismissed { reason }` · `signed_up { has_phone }` · `logged_in` ·
  `log_in_failed { code }` · `guest_merged { lessons, places }` · `password_reset_requested` · `password_reset_done` ·
  `signed_out`

### testIDs (app)
`auth.username`, `auth.password`, `auth.password-toggle`, `auth.phone`, `auth.terms`, `auth.submit`,
`auth.forgot-link`, `auth.code`, `auth.new-password`, `auth.gate`, `auth.gate-signup`, `auth.gate-login`,
`auth.gate-not-now`, `profile.guest-signup`, `profile.guest-login`

## Media
Existing canvas SVGs only: Irbis default, excited, proud, worried; panda cub (L1). To confirm at step 1 whether they are
final. No new art needed.

## Waivers
- none

## Out of scope
- Social log-in (Google/Apple), email, two-factor; username change; account deletion (with `profile`);
  web admin log-in screen (first web feature).

## Assumptions
- Q1 (owner, 2026-10-17): recovery by optional phone + SMS code; no phone = no self-service reset.
- Q2 (owner, 2026-10-17): log-in is asked for anything that saves or earns; browsing, lessons (without XP) open.
- Q3 (owner, 2026-10-17): guest onboarding choices, lesson progress and saved places move into the account.
- Q4 (owner, 2026-10-17): trusted account = older than 7 days (tour groups can't act together on day one).

## Open questions (asked at `/feature auth` step 1)
- Username rules: canvas draws "3–20 letters, numbers, dot or underscore" — confirm; reserved names; case-insensitive?
- Password policy: canvas draws "at least 8 characters, not your username" — confirm; max length; breached-password check?
- Lockout: how many failed log-ins, for how long?
- Reset code: expiry (e.g. 10 min), resend wait (canvas: 0:45), max attempts.
- SMS provider for reset codes (Eskiz, Play Mobile, …) — real credentials go in `.env` by the owner.
- Guest XP on merge: award lesson XP retroactively (current draft) or start XP at sign-up?
- Does a guest finishing a lesson see the A3 sheet immediately (canvas) or only a banner?
