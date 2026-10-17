# auth

- Status: Draft — awaiting approval (questions answered 2026-10-17)
- Surfaces: api | app (web admin log-in is out of scope — first web feature)
- Related ADRs: ADR-001 (auth), ADR-003 (API style)
- Requirements: Product Overview § Accounts & sign-in · Screens: `design/canvas/AccLogin`, `AccSignup`, `AccGate`,
  `AccForgot`, `AccReset`, `AccGuestProfile`, `Nav` (bottom tabs)

## Goal
Anyone can use Irbis without an account. A bottom tab bar is the app's home; the Profile tab lets a guest create an
account or log in (username + password), and a shared log-in prompt is ready for every later feature that saves or
earns. Forgotten passwords are reset with an SMS code when the account has a recovery phone.

## API
| Method | Path | Auth | Request | Response | Errors (code) |
|---|---|---|---|---|---|
| POST | /v1/auth/sign-up | public | username, password, recoveryPhone?, locale, acceptTerms | tokens + me | USERNAME_TAKEN, USERNAME_INVALID, USERNAME_RESERVED, PASSWORD_WEAK, TERMS_REQUIRED, VALIDATION_FAILED |
| GET | /v1/auth/username-available?u= | public, rate-limited | — | { available, reason? } | RATE_LIMITED |
| POST | /v1/auth/log-in | public | username, password | tokens + me | INVALID_CREDENTIALS, ACCOUNT_LOCKED (+ retryAfterSec), RATE_LIMITED |
| POST | /v1/auth/refresh | public (refresh token in body) | refreshToken | tokens | REFRESH_INVALID, REFRESH_REUSED |
| POST | /v1/auth/sign-out | user | refreshToken | 204 | — |
| POST | /v1/auth/password/forgot | public | username | 202 `{ resendAfterSec: 60 }` — identical whether or not the user/phone exists | RATE_LIMITED |
| POST | /v1/auth/password/reset | public | username, code, newPassword | tokens + me | CODE_INVALID, CODE_EXPIRED, CODE_ATTEMPTS, PASSWORD_WEAK |
| PUT | /v1/me/recovery-phone | user | phone | 202 (code sent) | PHONE_INVALID, RATE_LIMITED |
| POST | /v1/me/recovery-phone/verify | user | code | me | CODE_INVALID, CODE_EXPIRED, CODE_ATTEMPTS |
| GET | /v1/me | user | — | me { id, username, locale, hasRecoveryPhone, createdAt } | — |
| POST | /v1/me/guest-merge | user | { locale?, onboarding? } (extensible) | merged summary | VALIDATION_FAILED |

## Data model changes
`User` (username unique on `lower(username)`, passwordHash argon2id, recoveryPhone? encrypted at rest +
recoveryPhoneVerifiedAt?, locale, createdAt), `RefreshToken` (familyId, tokenHash, expiresAt, revokedAt, replacedById),
`PasswordReset` (userId, codeHash, expiresAt, attempts, usedAt), `LoginAttempt` (username, ip, at, ok),
`SmsCode` for phone verification (or shared with PasswordReset via a `purpose` column). Migration `auth_init`.
`SmsSender` interface: `FakeSmsSender` (dev/test only — logs `code for user …: 123456` to the API log; refuses to load
when `NODE_ENV=production` or `APP_ENV` is staging/prod), real adapter later with owner-provided `.env` keys.

## Acceptance criteria
- **AC1** — Cold start lands on the bottom tab bar (Path · Explore · Lessons · Community · Profile, per the canvas
  `Nav`) with no log-in wall. Path, Explore, Lessons and Community show their empty state with sleepy Irbis and
  "Coming with the next update" until their feature ships.
- **AC2** — Profile tab, guest: canvas A6 — "You're exploring as a guest", Create free account, Log in, Language,
  Safety & SOS (Safety opens its empty state until `safety-center`).
- **AC3** — Sign up (A2): username 3–20 chars `a–z 0–9 . _`, not starting/ending with a dot, case-insensitive unique,
  reserved names refused (admin, irbis, support, moderator, root, system, official); live availability while typing
  (pristine → validating → success/error); password 6–64 chars, not equal to the username, not in the common-password
  list; optional recovery phone (+998, 9 digits); terms checkbox required. Success logs the user in and returns to
  where sign-up started.
- **AC4** — Log in (A1) with username + password; wrong username or password shows one generic message ("Username or
  password is wrong"). After **5** wrong passwords for a username within 15 min, that username is locked for **15 min**
  and the message says how long; a per-IP limit stops trying many usernames. "Continue as guest" closes the screen.
- **AC5** — Forgot password (A4 → A5): entering a username shows the same "code sent" screen whether or not the
  account or phone exists; if a verified recovery phone exists, a 6-digit code is sent. The code is valid **5 min**,
  "Send again" unlocks after **60 s**, **3** wrong tries void it, max 5 codes per day per account. Correct code + new
  password (6–64) logs the user in and signs out every other session. A4 shows the support path for accounts without a
  phone.
- **AC6** — Signed-in Profile shows the username, a "Recovery phone" row (Add / verified ✓) and Sign out. Adding a
  phone sends a code; verifying it marks the phone verified. Sign out clears the Keychain and returns to the guest
  Profile (no wall).
- **AC7** — `useRequireAccount(reason)` opens the log-in prompt (A3: "Keep your …", Create free account, I have an
  account, Not now) for a guest; after sign-up/log-in the gated action continues once; "Not now" closes with nothing
  lost. For a signed-in user it runs the action immediately. A dev-only Debug screen (absent from prod builds) can
  open the prompt for QA.
- **AC8** — Guest data (today: app language; onboarding choices once onboarding exists) is stored on the device and
  sent once to `/v1/me/guest-merge` after the first sign-up or log-in on that device; later features register their
  own items.
- **AC9** — Tokens: access JWT ~15 min, opaque refresh token rotated on every refresh and stored hashed; reusing an
  old refresh token revokes its whole family; the app refreshes once on 401 and retries; on refresh failure it
  returns to the guest state with a toast.
- **AC10** — The Status screen (M0) is no longer the first screen; it is reachable in dev/staging builds through the
  Debug screen and the deep link `irbis://debug/status`.

### Required UI states (every touched client)
- [ ] Loading: submit buttons pending (no double submit); availability check spinner in the field
- [ ] Error: field errors under fields (server `fieldErrors` mapped); generic credential error; lock message with time
- [ ] Offline: sign-up / log-in / reset refused with a clear message; guest browsing continues
- [ ] Keyboard never covers inputs; `returnKeyType` chain; password show/hide; autofill types
      (username, password, new-password, one-time-code, tel)
- [ ] Tokens, Nunito, light/dark, safe areas; `src/shared/components` primitives only

### QA events (app, dev/staging builds)
`auth_gate_shown { reason }` · `auth_gate_dismissed { reason }` · `signed_up { has_phone }` · `logged_in` ·
`log_in_failed { code }` · `guest_merged { items }` · `password_reset_requested` · `password_reset_done` ·
`recovery_phone_verified` · `signed_out` · `tab_opened { tab }`

### testIDs (app)
`nav.tab-path`, `nav.tab-explore`, `nav.tab-lessons`, `nav.tab-community`, `nav.tab-profile`,
`auth.username`, `auth.username-status`, `auth.password`, `auth.password-toggle`, `auth.phone`, `auth.terms`,
`auth.submit`, `auth.error`, `auth.forgot-link`, `auth.continue-guest`, `auth.code`, `auth.resend`,
`auth.new-password`, `auth.gate`, `auth.gate-signup`, `auth.gate-login`, `auth.gate-not-now`,
`profile.guest`, `profile.guest-signup`, `profile.guest-login`, `profile.username`, `profile.recovery-phone`,
`profile.sign-out`, `debug.open-gate`, `empty.coming-soon`

## Media
`design/media/auth/MEDIA.md` — all from the canvas, owner confirmed final (2026-10-17).

## Waivers
- Bottom tabs for Path / Explore / Lessons / Community show an intentional "coming with the next update" empty state
  (owner decision Q6) — not a placeholder to be flagged by review; each feature replaces its tab's content.

## Out of scope
- Social log-in, email, two-factor, username change, account deletion (with `profile`), web admin log-in screen,
  real SMS provider adapter (owner adds keys later), onboarding screens.

## Assumptions
- Q1 (owner, 2026-10-17): recovery by optional phone + SMS code; no phone = no self-service reset.
- Q2 (owner, 2026-10-17): log-in is asked for anything that saves or earns; browsing and lessons (no XP) open.
- Q3 (owner, 2026-10-17): guest progress moves into the account.
- Q4 (owner, 2026-10-17): trusted account = older than 7 days.
- Q5 (owner, 2026-10-17): username 3–20 `a–z 0–9 . _`, case-insensitive, reserved names; password 6–64, not the
  username, common passwords blocked; 5 wrong tries → 15-min lock; reset code 5 min, resend 60 s, 3 tries.
- Q6 (owner, 2026-10-17): bottom tabs now with a real Profile tab; other tabs show the coming-soon empty state.
- Q7 (owner, 2026-10-17): SMS sender pluggable; dev uses a fake that logs the code locally (never staging/prod).
- Q8 (owner, 2026-10-17): log-in prompt built as a shared hook + sheet, dev Debug trigger for QA.
- Q9 (owner, 2026-10-17): guest-merge mechanism now (language today); later features add their items and XP rules.
- Q10 (owner, 2026-10-17): canvas mascot / panda / nav icons are final art.
