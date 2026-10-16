# ADR-002: Database and migrations

- Status: Proposed
- Date: 2026-10-16

## Decision
PostgreSQL with Prisma. Schema changes only through `prisma migrate dev --name <change>` producing a new migration.

- Never edit or delete an existing migration. Fix forward with a new one.
- `prisma db push` only against a throwaway local DB, never shared/staging/prod.
- Prisma client is used only inside `*.repository.ts` files.
- Seeds use synthetic data only (`guest_1`, `+998XXXXXXXXX`). No production exports, ever.
- Geo data: store lat/lng as `Decimal`/`Float`; distance checks in the service layer
  (revisit PostGIS if we need spatial queries at scale — would be a new ADR).

## Why
Reviewable, reproducible schema history; a single DB access layer keeps business logic testable.
