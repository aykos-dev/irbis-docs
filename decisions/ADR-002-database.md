# ADR-002: Database and migrations

- Status: Accepted (owner, 2026-10-17)
- Date: 2026-10-16

## Decision
PostgreSQL with Prisma. Schema changes only through `prisma migrate dev --name <change>` producing a new migration.

- Never edit or delete an existing migration. Fix forward with a new one.
- `prisma db push` only against a throwaway local DB, never shared/staging/prod.
- Prisma client is used only inside `*.repository.ts` files.
- Seeds use synthetic data only (`guest_1`, `+998XXXXXXXXX`). No production exports, ever.
- Geo data: store lat/lng as `Decimal`/`Float`; distance checks in the service layer
  (revisit PostGIS if we need spatial queries at scale — would be a new ADR).

- Local dev and e2e tests: Postgres 17 in Docker (`docker compose up -d db` in irbis-api; Testcontainers for e2e).
  Docker Desktop must be running.

## Why
Reviewable, reproducible schema history; a single DB access layer keeps business logic testable.
