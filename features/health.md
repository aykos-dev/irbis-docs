# health

- Status: Approved (M0 reference feature, owner started M0 on 2026-10-17)
- Surfaces: api | web | app
- Related ADRs: ADR-001 (guard: `/health` is `@Public()`), ADR-002, ADR-003
- Requirements: none in the Product Overview — this is the **reference pattern** every later feature copies
  (contract → codegen → hook → screen with all four states → tests → QA events → testIDs).

## Goal
The app and the admin web show whether the API and its database are reachable, using the full production pattern.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /health | public | — | `{ status: "ok" \| "degraded", db: "up" \| "down", version: string, time: ISO-8601 }` | 503 with the same body when the DB is down |

`operationId: Health_check`. Unversioned (infrastructure), excluded from request logs, included in `openapi.json`.

## Data model changes
None (first migration creates nothing feature-specific; Prisma is wired and `SELECT 1` proves the connection).

## Acceptance criteria
- **AC1** — `GET /health` returns 200 `{ status: "ok", db: "up", version, time }` when Postgres is reachable.
- **AC2** — With Postgres stopped, it returns 503 `{ status: "degraded", db: "down", … }` within 3 s (no hang).
- **AC3** — The app's **Status** screen (initial route in M0) shows: loading skeleton → "API is up · Database is up ·
  v{version}" with a Go-style chip; on API unreachable an error state with Retry; offline (no network) a persistent
  offline banner, not a toast. Pull to refresh refetches.
- **AC4** — Copy is in uz / ru / en via i18n keys (`health.*`); the language follows the device locale in M0.
- **AC5** — The web admin dashboard (`/`) shows the same status card with loading / error + retry / offline states.
- **AC6** — Both clients call the API only through the orval-generated hook (`useHealthCheck`); no hand-written types.
- **AC7** — The app logs `health_checked { status, db }` through `qaLog` in dev/staging builds.

### Required UI states (every touched client)
- [ ] Loading (skeleton)
- [ ] Empty — n/a (single object)
- [ ] Error (message + retry)
- [ ] Offline (banner; cached result stays visible, marked stale)
- [ ] App: safe areas; light + dark from tokens; Nunito; press state on Retry
- [ ] Uses design tokens and `src/shared/components` primitives only

### QA events (app, dev/staging builds)
- `health_checked { status, db }`
- `location_received { is_mocked, accuracy_m }` — **not** in M0 (no location yet); added with the first location feature.

### testIDs (app)
`health.status-card`, `health.api-chip`, `health.db-chip`, `health.version`, `health.retry`, `app.offline-banner`

## Media
None (Irbis default SVG from the canvas on the status card — `design/assets.md` `9ebec15f…`).

## Waivers
- Haptics, Toast, bottom tabs, deep links: their shared primitives are scaffolded in M0, but the Status screen has no
  mutation, so no toast/haptic is fired.

## Out of scope
- Bottom navigation tabs and real screens (each arrives with its feature); auth; push.

## Assumptions
- Q1 (owner, 2026-10-17): app id `uz.irbis.app` (+ `.dev` / `.staging` suffixes).
- Q2 (owner, 2026-10-17): Postgres 17 in Docker Desktop for dev and e2e (Testcontainers).
- Q3 (owner, 2026-10-17): M0 verified on the owner's Galaxy S25 Ultra (Android 16) only; iOS project generated, not built.
