# Brief check-in-2-irbis-api — demo accounts (ADR-006)

- Spec: features/check-in.md · ACs: AC6, AC8 (api side) · ADR: decisions/ADR-006-demo-accounts.md
- Repo / branch: irbis-api · `feat/check-in` (stacks on brief 1)
- Depends on: check-in-1-irbis-api (`checkIn.config.demoPerIpPerDay`)

## Files
- Touch: `src/features/auth/` (service, controller, dto, errors; me service/dto) · `prisma/schema.prisma` + new
  migration `demo_accounts`
- Read for patterns: `auth.service.ts` `signUp` (tokens, session, response shape), username rules + reserved names,
  `@Throttled('auth')`, `@ClientIp()`, `PasswordService`, log-in path

## Behaviour
- `User.passwordHash` nullable; `User.isDemo Boolean @default(false)`.
- `POST /v1/auth/demo` (`@Public`, `@Throttled('auth')`) body `{ locale: uz|ru|en }` → creates a user with username
  `explorer_<n>` (n random 4 digits, 6 digits after 5 collisions; must pass the reserved-name rules), no password,
  isDemo true, locale; returns exactly what sign-up returns (201). More than `demoPerIpPerDay` (5) demo accounts
  from one client IP in the last 24 h → 429 `DEMO_LIMIT` (count users with isDemo created from that IP: store the
  creation IP hash or a small `demo_creations` table — your call, no raw IP in logs).
- Log-in with a user that has no passwordHash → same error as a wrong password (no timing shortcut: still run a
  dummy hash compare). Password reset / recovery phone flows refuse demo users the same way.
- `POST /v1/me/secure` (user) `{ username, password }`: user not demo → 409 `NOT_DEMO`; username taken → 409
  `USERNAME_TAKEN`; same validation as sign-up; sets username + password hash, isDemo false, keeps the session.
  Returns `MeResponseDto`. operationIds `authCreateDemo`, `meSecure`.
- `MeResponseDto` gains `isDemo`. Admin user DTOs: add `isDemo` if trivial, else skip.

## Done when
- [ ] unit: username generation + collision retry, secure rules
- [ ] e2e: demo 201 → /v1/me isDemo true → guest-merge works → secure 200 → log-in with the new password 200;
  log-in as demo before securing → 401; 6th demo from one IP → 429 DEMO_LIMIT; secure on a normal user → 409
- [ ] `npm run check` green, `npm run openapi:export` committed, commits on `feat/check-in`
