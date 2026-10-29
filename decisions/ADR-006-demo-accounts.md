# ADR-006 — Demo accounts for guests who check in

- Status: Accepted (owner, 2026-10-29)
- Amends: ADR-001 (guest-first, username + password)

## Context
ADR-001 keeps guests account-less on the server: guest data lives on the phone and merges on sign-up / log-in.
Check-ins are the core earning action and usually happen offline on a mountain. The owner wants a guest's
check-ins kept and credited without forcing sign-up first (2026-10-29, `check-in` Q4/Q5).

## Decision
- A guest's check-in is stored on the phone (verified GPS fix, queued like waypoints).
- When the first queued check-in can be sent (online), the app creates a **demo account**:
  `POST /v1/auth/demo` → a real user with an auto username `explorer_<4–6 digits>`, **no password**, `isDemo: true`,
  and normal access + refresh tokens. The app then runs the existing guest merge (`/v1/me/guest-merge`) and sends
  the queued check-ins.
- A demo account is a normal account for everything else (XP, levels, lessons, streaks, path, trips).
- It cannot log in with a password. Profile shows the username and **Secure your account**:
  `POST /v1/me/secure { username, password }` sets a chosen username + password and clears `isDemo`.
- Signing out of a demo account (or losing the phone) loses it; the app warns before sign-out.
- Guests who never check in stay account-less exactly as in ADR-001.

## Why
Keeps guest-first (no form before the first summit) while the server stays the only place XP and level facts are
granted. A demo account reuses every existing account path instead of adding a second "guest progress" store.

## Consequences
- `User.passwordHash` becomes nullable; `User.isDemo` added. Log-in refuses users without a password hash.
- `/v1/auth/demo` is public: throttled per IP (auth throttle + 5 demo accounts per IP per day, server config).
- Abandoned demo accounts accumulate; a cleanup job is a later decision (not built).
- "Trusted account = older than 7 days" counts from demo creation.
