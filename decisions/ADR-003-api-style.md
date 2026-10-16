# ADR-003: API style and contract

- Status: Accepted (owner, 2026-10-17)
- Date: 2026-10-16

## Decision
REST + JSON under `/v1`, documented by `@nestjs/swagger`. The API writes `openapi.json` to its repo root
(`npm run openapi:export`); that committed file is the contract.

- Web and app generate clients with **orval** (TanStack Query hooks + types) into `src/shared/api/generated/`.
  Generated code is never hand-edited. No ad-hoc `fetch`.
- Every request body/query is a DTO with class-validator; global `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true })`.
- One global exception filter → `{ statusCode, code, message, fieldErrors?, requestId }`; clients branch on `code`.
- Mutations accept an `Idempotency-Key` header; value-granting endpoints store and replay it.
- Pagination: `?cursor=&limit=` → `{ items, nextCursor }`.
- Breaking changes need a new ADR or a `/v2` route.

## Why
Codegen is free, deterministic and cannot invent a field name; contract drift becomes a compile error in clients.
