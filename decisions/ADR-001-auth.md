# ADR-001: Authentication — username + password, guest-first

- Status: Accepted (owner, 2026-10-17) — replaces the earlier phone/OTP proposal
- Date: 2026-10-17

## Decision
**Guest-first.** The app is fully explorable without an account: places, conditions, Explore map, feed, lessons.
SOS and the Safety center always work without an account. The app asks to log in only when an action saves or earns
(check in, start a trip plan, earn XP or badges, post, like, comment, join a group, play online games), with a sheet
offering Create account / Log in / Not now (canvas A3 `AccGate`).

**Credentials.** Username + password. A recovery phone is **optional** and used only for password reset by a 6-digit
SMS code; without one there is no self-service reset (support handles it). No social login, no email (for now).

**Guest data** (onboarding choices, lesson progress, saved places) is kept on the device and merged into the account on
sign-up or log-in.

**Trusted account** (counts for fair likes and auto-hide reports) = account older than 7 days. Reason: Irbis is
recommended on tours, so a whole group can sign up at once; the delay stops them pushing or hiding a post on day one.

**Tokens** (unchanged): short-lived JWT access token (~15 min) + opaque refresh token with rotation and reuse
detection, stored hashed in Postgres. Mobile keeps both in Keychain / Keystore (`react-native-keychain`); the web
admin keeps the access token in memory and the refresh token in an httpOnly, Secure, SameSite cookie. Global
deny-by-default guard; guest-readable endpoints are explicitly `@Public()`. Roles: `user`, `admin` (+ `operator` later).

**Passwords.** Hashed with Argon2id (per-user salt, parameters in config). Login and reset endpoints rate-limited per
username and per IP; failed-attempt lockout. Reset codes: 6 digits, single use, short expiry, attempt-limited, hashed
at rest. A password reset revokes all refresh tokens ("logged out on your other phones").

## Why
Login walls lose first-time explorers before they see value; Irbis's value (where to go, is it safe) is readable
without an account, while progress, trips and community need identity. Username + password works without an SMS
provider for sign-up; the optional phone covers recovery for people who want it.

## Consequences
- Every endpoint that writes or awards is authenticated; reads guests need are `@Public()` and reviewed as such.
- The app keeps a local guest store and a merge step at sign-up/log-in (`auth` feature); XP for guest-time actions is
  awarded on merge under the normal caps.
- No phone means some users can lose access permanently — the sign-up screen says so and Settings nudges to add one.
- Values to confirm at `/feature auth`: username rules, password policy, lockout thresholds, code expiry, what a
  "Not now" guest sees on the gated screen afterwards.
