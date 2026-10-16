# Irbis — Project

## Product
<!-- FILL IN: 3–5 sentences. Who uses it, what problem it solves, the core loop. -->
Irbis is a mobile app (Expo) with an admin web panel (Next.js) backed by one API (NestJS).
Example capability: users check in at verified spots and earn XP; admins manage spots and see stats.

## Surfaces
- **app** — end users, iOS + Android.
- **web** — admin / back-office only.
- **api** — the only thing that touches the database.

## Stack (pin exact versions at scaffold time, then update this table)
Latest on npm as of 2026-10-16 shown for reference. Replace with what you actually installed.

| Area | Package | Pinned |
|---|---|---|
| Runtime | Node | 22.x LTS |
| Package manager | npm | 10.x |
| Language | TypeScript (strict) | _ (latest seen 7.0.2) |
| API | @nestjs/core / @nestjs/cli | _ (12.1.3 / 12.0.8) |
| DB | PostgreSQL | _ |
| ORM | Prisma | _ (check stable tag, latest was an rc) |
| API docs | @nestjs/swagger → `openapi.json` | _ |
| Web | Next.js (App Router) | _ (16.4.2) |
| App | Expo SDK / Expo Router / React Native | _ (58 / _ / 0.88) |
| Server state | @tanstack/react-query | _ (5.104.3) |
| Codegen | orval | _ (8.43.0) |
| Tests | Vitest (web/app units), Jest or Vitest (api) | _ |
| Lint | ESLint flat config + eslint-plugin-boundaries | _ (10.12 / 7.2) |
| Architecture | dependency-cruiser | _ (18.6) |

Rule: if code or memory disagrees with this table, the table wins. Check Context7 docs for that version.

## Conventions
- Feature slug: kebab-case (`spot-checkin`). Same slug for spec file, branch `feat/<slug>`, and `src/features/<slug>/` in every repo.
- Files: kebab-case. Classes/components: PascalCase. DB tables: snake_case plural; Prisma models PascalCase singular.
- API routes: `/v1/<resource>` plural nouns, kebab-case. JSON: camelCase. Dates: ISO-8601 UTC.
- Errors: API returns `{ statusCode, error, message, details? }` via one global exception filter.
- Commits: Conventional Commits (`feat(spots): …`, `fix(auth): …`).

## Folder rules
**api** — `src/features/<slug>/` = `*.controller.ts` (thin) → `*.service.ts` (logic) → `*.repository.ts` (Prisma only here) + `dto/`.
`src/common/` for guards, filters, interceptors, decorators. `src/lib/` for shared helpers. `prisma/` for schema + migrations.

**web / app** — `src/features/<slug>/` (screens, components, hooks for that feature only).
`src/api/generated/` (orval output, never edited). `src/components/ui/` shared primitives. `src/lib/` helpers.
`src/theme/tokens.ts` the only place for colours, spacing, radii, typography.
Features never import each other's internals; shared code moves to `ui/` or `lib/`.

## Environments
local → staging → production. Config only via env vars. Real values live in each repo's `.env` (git-ignored),
filled in by a human, and in the secrets manager for deployed environments. Never in chat or code.
