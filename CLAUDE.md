# Irbis — cross-repo working rules

You are launched from `irbis-docs` (the project brain) with the code repos added:
`claude --add-dir ../irbis-api ../irbis-web ../irbis-app` (or `./scripts/start.sh`).

## Start of every session
1. Read `STATUS.md`. Then `PROJECT.md` and only the `decisions/` ADRs relevant to the task.
2. Context lives in files and git, never in chat. One feature per session, then `/clear`.

## Repos
| Repo | Role | Agent |
|---|---|---|
| `irbis-docs` | specs, ADRs, status, Claude config | main session |
| `irbis-api` | NestJS + Postgres + Prisma, exports `openapi.json` | `api-dev` |
| `irbis-web` | Next.js admin | `web-dev` |
| `irbis-app` | bare React Native (no Expo) | `app-dev` |

- Not a monorepo. Never copy code or types between repos.
- `irbis-api/openapi.json` is the single source of truth for the contract.
  Web and app get types/hooks only via `npm run gen:api` (orval). Never hand-write API types.
- Same feature slug and folder in every repo: `src/features/<slug>/`.
- Delegate repo work to that repo's subagent; keep the main session small.
- Each code repo has `docs/architecture.md` + `docs/engineering-standards.md`. They are binding:
  every change follows the architecture, and the standards' Quick gate is the definition of done.
- Design tokens: `design/design.md` is the source of truth for web and app.

## Commands
- `/feature <slug> — <behaviour>`: spec → approval gate → api → clients → review → wrap up.
- `/bugfix <error/log + failing behaviour> | <slug>/D{n}`: reproduce with a failing test, then fix.
- `/qa-plan <slug>`: concrete, AC-traced Android test plan → `qa/<slug>/cases/`.
- `/qa-run <slug> [build]`: run it on the Android phone, proof per case, defects → `qa/<slug>/bugs/D{n}_…/`.
- `/qa-retest <slug>/D{n} … | open`: re-check logged defects on a new build (Fixed / Not fixed / Not reached).
  Loop: `/qa-run` → `/bugfix <ref>` → `/qa-retest <ref>`. Index of all defects: `qa/BUGS.md`. iOS: by hand.
- Every repo: `npm run check` (quiet: lint + typecheck + tests + slop grep). `npm run gen:api` in web/app.

## Hard rules
- Never modify or skip an existing test to make it pass. Report it instead.
- Ask before adding any package.
- Only create new migrations; never edit an existing one; never `prisma db push` outside a throwaway local DB.
- No `any`, `@ts-ignore`, `eslint-disable`, `TODO`/`FIXME`/mock data in `src/` (tests excepted).
- Secrets only from env vars. Never read `.env*`. Never ask for or print a secret value; use placeholders.
- No guest/employee personal data in fixtures, seeds, logs or docs — synthetic data only (`guest_1`, `+998XXXXXXXXX`).
- irbis-app is bare React Native: no Expo packages, Expo Router, EAS or prebuild.
- Surgical changes only: nothing outside the spec's scope, no drive-by refactors.
- Before creating a helper/component, check the repo's shared modules listed in its CLAUDE.md.
- Uncertain about a framework API? Use Context7 docs for the version pinned in `PROJECT.md`.
- "Done" means `npm run check` passed and its output is pasted in the summary.
- Commit locally, never push. Never change decisions in `decisions/` silently — propose a new ADR.

## Slop checklist (reviewer uses this)
1. Test diffs: existing tests edited/deleted/skipped? Everything mocked so nothing real is tested?
2. Contract: clients use generated hooks only; no hand-written fetch or API types.
3. Verified: check output present and green in every touched repo.
4. Duplicates: new util/component that already exists in `src/lib` or `src/components/ui`?
5. Scope: anything beyond the spec, or drive-by refactors?
6. Versions: outdated Next.js / React Native / React Navigation / Nest / Prisma patterns? Any Expo in irbis-app?
7. Dependencies: new packages without approval?
8. Errors: swallowed errors, `catch { return null }`, `console.log` as handling?
9. Placeholders: TODO, mock data, hardcoded IDs/URLs?
10. Security: endpoint without guard (not explicitly `@Public()`), missing DTO validation, CORS `*`, secrets in code, PII in logs.
11. Migrations: old migration edited? destructive change without a plan?
12. UI states: loading / empty / error / offline, keyboard + safe areas (app), design tokens used.
13. Standards: each touched repo's `docs/engineering-standards.md` Quick gate passes or has a written waiver.
