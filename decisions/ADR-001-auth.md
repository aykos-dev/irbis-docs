# ADR-001: Authentication

- Status: Proposed
- Date: 2026-10-16

## Decision
JWT access tokens (short-lived, ~15 min) + opaque refresh tokens with rotation and reuse detection,
stored hashed in Postgres. Not server sessions.

- Mobile (bare RN) stores both tokens in the Keychain / Android Keystore via `react-native-keychain` — never MMKV.
- Web admin keeps the access token in memory; the refresh token is an httpOnly, Secure, SameSite cookie
  set by the API (web and API share a registrable domain).
- Auth guard is global and deny-by-default. Open routes must use `@Public()`.
- Roles via a `@Roles()` decorator + guard (`user`, `admin`). Admin web requires `admin`.
- Signing keys come from env vars / secrets manager only.

## Why
Mobile clients need long-lived sign-in without cookies; rotation limits stolen-token damage;
global guard means a forgotten decorator fails closed, not open.

## Consequences
Every new endpoint is protected unless explicitly marked public; the reviewer checks every `@Public()`.
