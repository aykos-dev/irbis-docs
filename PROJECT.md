# Irbis — Project

## Sources of truth
- **Requirements:** Claude Doc [Irbis — Product Overview](https://claude.ai/artifact/3Y8X76bzR6UE58fHkAdm1p) (read 2026-10-16; Accounts & sign-in added 2026-10-17, rev 32).
- **Design:** canvas [Irbis — Mobile App UI](https://claude.ai/artifact/CuodB816iZnDTUej2UiALf) (snapshot in `design/canvas/`, version 1792220545-f5f0, 2026-10-17).
- When those change, re-sync the affected spec in `features/` — the specs, not memory, drive the code.

## Product
Irbis is a Duolingo-style, gamified outdoor app that gets people in Uzbekistan and Central Asia out to peaks,
trails, caves, lakes and camping zones — and back home safely. It tells you where to go this week (matched to
level, season and forecast), whether it is safe right now, teaches safety in 3-minute lessons, keeps you safe on
the trail (trip plans, auto-alerts, SOS, offline maps), connects you with people to go with, and lets explorers
grow a community-verified map.

**Core loop:** learn → plan → go → check in → share → level up → unlock harder places (→ learn the next safety tier).
Real outdoor activity always earns the most XP; sofa activity earns small, capped XP. Nothing paid or grindable
unlocks a harder mountain — levels need XP **and** safety lessons **and** verified check-ins at the right difficulty.

**Who it's for:** beginners (18–35, first hikes), weekend hikers, experienced explorers, and later tour operators
and rental shops (marketplace).

**Brand:** Irbis, a chibi snow-leopard cub with a tiny orange backpack, in 5 expressions (excited, proud, worried,
sleepy, sad-but-cute). Glacier teal + sunrise orange, Nunito, chunky rounded buttons with a 4 px bottom shadow.
Tone: friendly, short sentences, never guilt. Tokens: `design/design.md`.

## Surfaces
- **app** — end users, iOS + Android, 390×844 design base, light + dark. Bare React Native — **no Expo**.
  Bottom nav: Path · Explore · Lessons · Community · Profile.
- **web** — Irbis admin panel (places, conditions, spot verification, moderation queue, commissions, settings) and,
  later, the operator dashboard. The admin panel has **no design yet**; build it from the design tokens.
- **api** — the only thing that touches the database; also runs scheduled jobs (weekly path, conditions, auto-alerts,
  league/Top Shots rounds).

## Binding per-repo docs
Every change in a code repo follows that repo's:
- `docs/architecture.md` — stack, structure, domain, decisions
- `docs/engineering-standards.md` — definition of done (Quick gate)

Design tokens for web and app: `design/design.md`. Canvas rules and numbers beyond the doc: `design/canvas-rules.md`.

## Locales, time, money
- **Locales:** Uzbek (uz, Latin), Russian (ru), English (en) — chosen in onboarding. i18n from the first feature;
  no hardcoded strings. Layouts must survive Russian/Uzbek length (design: buttons wrap, never truncate).
- **Time:** stored UTC; every product day/week boundary (daily game reset, Monday path rebuild, Top Shots rounds,
  streak days, league weeks) is **Asia/Tashkent** unless a spec says otherwise.
- **Money:** UZS (so'm), integers. XP, gems, elevation: integers.

## Product rules every feature must respect
- **Guest-first (ADR-001):** everything readable works without an account; log-in is asked only when an action saves
  or earns (check in, trip plan, XP/badges, post, like, comment, join a group, online games) via the log-in prompt
  sheet. SOS and the Safety center never require an account. Guest progress merges into the account on sign-up.
- **Accounts:** username + password; recovery phone optional (SMS reset code only). Trusted account = older than 7 days.
- Safety features (trip plans, auto-alerts, SOS, condition statuses) are free forever; no ads on safety screens.
- Condition status is always colour + icon + label (Go / Caution / Not now / Seasonal lock).
- "Not now" places never get a "Go there" button. Fragile spots never get map pins in feed or games.
- Photo location data is stripped from public copies.
- XP numbers and level thresholds in the doc are a **starting point, decided after testing** — keep them in
  server config, never hard-coded in clients.

## Stack summary (details and versions in each repo's architecture.md)
Latest stable on npm as of 2026-10-16. Replace with exact installed versions at scaffold time.

| Area | Choice |
|---|---|
| Runtime / PM | Node 22 LTS, npm 10 |
| Language | TypeScript strict everywhere |
| API | NestJS 12, Prisma 7.10 (stable, not 8.0 RC) + Postgres, @nestjs/swagger → `openapi.json` |
| Web | Next.js 16 App Router, Tailwind 4 + shadcn/ui, next-intl, Vitest — admin panel |
| App | React Native 0.88 bare (New Arch, Hermes), React Navigation 7, Reanimated 4, i18n-js, Jest |
| Shared client pattern | orval → TanStack Query 5 hooks + zod over one axios instance |
| Lint / architecture | ESLint flat + eslint-plugin-boundaries; dependency-cruiser in API |

Rule: if code or memory disagrees with a repo's architecture.md, the doc wins. Check Context7 for that version.

## Conventions
- Feature slug: kebab-case (`check-in`). Same slug for spec file, branch `feat/<slug>`, and `src/features/<slug>/` in every repo.
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
