# Irbis — Project

## Product
<!-- FILL IN: 3–5 sentences. Who uses it, what problem it solves, the core loop. -->
Irbis is a mobile app (bare React Native) with an admin web panel (Next.js) backed by one API (NestJS).
Example capability: users check in at verified spots and earn XP; admins manage spots and see stats.

## Surfaces
- **app** — end users, iOS + Android. Bare React Native — **no Expo**.
- **web** — admin / back-office only.
- **api** — the only thing that touches the database.

## Binding per-repo docs
Every change in a code repo follows that repo's:
- `docs/architecture.md` — stack, structure, domain, decisions
- `docs/engineering-standards.md` — definition of done (Quick gate)

Design tokens for web and app: `design/design.md`.

## Locales
<!-- CONFIRM: assumed uz, ru, en. Default: ? -->
i18n is required from the first feature in web and app; no hardcoded strings.

## Stack summary (details and versions in each repo's architecture.md)
Latest stable on npm as of 2026-10-16. Replace with exact installed versions at scaffold time.

| Area | Choice |
|---|---|
| Runtime / PM | Node 22 LTS, npm 10 |
| Language | TypeScript strict everywhere |
| API | NestJS 12, Prisma 7.10 (stable, not 8.0 RC) + Postgres, @nestjs/swagger → `openapi.json` |
| Web | Next.js 16 App Router, Tailwind 4 + shadcn/ui, next-intl, Vitest |
| App | React Native 0.88 bare (New Arch, Hermes), React Navigation 7, Reanimated 4, i18n-js, Jest |
| Shared client pattern | orval → TanStack Query 5 hooks + zod over one axios instance |
| Lint / architecture | ESLint flat + eslint-plugin-boundaries; dependency-cruiser in API |

Rule: if code or memory disagrees with a repo's architecture.md, the doc wins. Check Context7 for that version.

## Conventions
- Feature slug: kebab-case (`spot-checkin`). Same slug for spec file, branch `feat/<slug>`, and `src/features/<slug>/` in every repo.
- Files: kebab-case (API, web), PascalCase for RN components/screens. DB tables: snake_case plural; Prisma models PascalCase singular.
- API routes: `/v1/<resource>` plural nouns, kebab-case. JSON: camelCase. Dates: ISO-8601 UTC.
- Errors: `{ statusCode, code, message, fieldErrors?, requestId }`; clients branch on `code`.
- Money / points: integers, never floats.
- Commits: Conventional Commits (`feat(spots): …`, `fix(auth): …`).

## Folder rules (summary)
**api** — `src/features/<slug>/` = controller (thin) → service (logic) → repository (Prisma only) + errors + `dto/`.
**web / app** — `src/app/` shell/routes, `src/features/<slug>/`, `src/shared/` (api incl. `generated/`, components, hooks, i18n, utils/lib, tokens).
Features never import each other; shared code moves to `shared/` (or `common/`/`lib/` in the API).

## Environments
local → staging → production. Config only via env vars. Real values live in each repo's `.env` (git-ignored),
filled in by a human, and in the secrets manager for deployed environments. Never in chat or code.
