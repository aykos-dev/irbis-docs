# Setup (M0, done once by hand)

## Already prepared (2026-10-16)
- `irbis/` plain folder with four sibling git repos (`main` branch, nothing pushed).
- `irbis-docs`: CLAUDE.md, PROJECT.md, ROADMAP.md, STATUS.md, ADR-001..003, spec template,
  `/bugfix` command, agents `api-dev`, `web-dev`, `app-dev` (sonnet), `reviewer` (opus).
- Hooks: PreToolUse blocks `.env*`, key files, `node_modules`/build dirs; Stop runs `npm run check`
  in every repo with changes (blocks once, then lets Claude report).
- Each code repo: short CLAUDE.md, `docs/architecture.md`, `docs/engineering-standards.md`, and
  `.claude/settings.json` (same deny rules + its own Stop hook).
- User-level (global): plugin `andrej-karpathy-skills`, MCP `context7` (current framework docs).

## Launch
```bash
cd ~/work/irbis/irbis-docs && ./scripts/start.sh
```
(`.claude/settings.json` also lists the three repos in `additionalDirectories`, so plain `claude` works too.)

## Remaining by-hand steps, in order
Every code repo already has `docs/architecture.md` + `docs/engineering-standards.md` — scaffold to match them.
Generators refuse non-empty folders, so scaffold into a temp dir and copy over (keep the existing
`CLAUDE.md`, `docs/` and `.claude/`), or move those aside and back.

1. **API** (`irbis-api/docs/architecture.md`):
   `npx @nestjs/cli new irbis-api --package-manager npm --strict --skip-git`, then (after approval)
   `@nestjs/swagger @nestjs/config @nestjs/throttler @nestjs/terminus nestjs-pino pino-http helmet
   class-validator class-transformer zod prisma@7 @prisma/client@7 @prisma/adapter-pg`, dev: `testcontainers supertest dependency-cruiser`.
   Add `docker-compose.yml` (Postgres), `scripts/export-openapi.ts` + `"openapi:export"`, global guard/filter/pipe.
2. **Web** (`irbis-web/docs/architecture.md`):
   `npx create-next-app@latest irbis-web --ts --app --src-dir --tailwind --eslint --use-npm --no-git`,
   then `npx shadcn@latest init`, `@tanstack/react-query @tanstack/react-table axios react-hook-form zod sonner next-intl`,
   dev: `orval vitest @testing-library/react msw eslint-plugin-boundaries`.
3. **App — bare React Native, no Expo** (`irbis-app/docs/architecture.md`):
   `npx @react-native-community/cli@latest init Irbis --directory irbis-app --pm npm --skip-git-init --install-pods false`
   (pick the RN version explicitly with `--version 0.88.x`). Then the libraries in the architecture's
   stack table, `cd ios && LANG=en_US.UTF-8 pod install`, and run both `npm run ios` and `npm run android`
   before adding anything else. Configure schemes/flavours for development / staging / production.
4. **`npm run check` in all three** — quiet, failures only, e.g.
   ```json
   "lint": "eslint . --quiet",
   "typecheck": "tsc --noEmit --pretty false",
   "test:ci": "vitest run --reporter=dot --silent",
   "slop": "! grep -rnE 'TODO|FIXME|@ts-ignore|eslint-disable|\\bmock' src --include='*.ts' --include='*.tsx' --exclude-dir=__tests__ --exclude='*.spec.*' --exclude='*.test.*' --exclude-dir=generated",
   "check": "npm run -s lint && npm run -s typecheck && npm run -s test:ci && npm run -s slop"
   ```
   Jest repos (API, app): `jest --silent --reporters=summary`. App adds `! grep -rn "from 'expo" src` to `slop`.
   ESLint: `no-explicit-any`, `ban-ts-comment`, `--no-inline-config`, `eslint-plugin-boundaries` for the
   folder rules; web bans arbitrary Tailwind values; dependency-cruiser in the API keeps Prisma in repositories.
5. **`gen:api`** in web and app: `orval.config.ts` → input `../irbis-api/openapi.json`, output
   `src/shared/api/generated`, client `react-query` + `zod`, mutator `src/shared/api/client.ts`.
6. **`.env.example`** in each repo with variable names only. Fill the real `.env` yourself; never paste values into chat.
7. **Pin versions** you actually installed into each repo's `docs/architecture.md` stack table; set ADR-001..003 to Accepted.
8. **Design**: fill `design/design.md` tokens, mirror into `irbis-app/src/shared/constants/*` and
   `irbis-web/src/shared/styles/tokens.css`; add 2–3 reference screens in `design/`.
9. **Reference feature** `health` end to end by hand (API endpoint → openapi → gen:api → web + app screen
   with all four states). Every later feature copies this pattern.

## Admin account (before using the admin web, feature `auth`)
The first admin is created from the API repo; there is no public way to make one.
1. Start the local database and apply migrations: `cd ../irbis-api && docker compose up -d db && npx prisma migrate deploy`
   (your `.env` supplies `DATABASE_URL`).
2. Run `npm run admin:create` **in an interactive terminal**. It asks for the username, then the password twice
   (typing is hidden). It never takes the password as an argument, environment variable or pipe.
3. If the username already exists it offers to promote that user to admin (their password stays unchanged).
   Reserved names such as `admin` are allowed here (the public sign-up refuses them).
4. Sign in at the admin web with that account. Further admins: promote users from the admin panel (user detail,
   change role) or run the command again.
Staging/prod additionally need `APP_ENV=staging|prod` and `PHONE_ENCRYPTION_KEY` (`openssl rand -base64 32`),
set in the secrets manager — never pasted into chat. The fake SMS sender refuses to start there.

## Later (not day one)
- **Graphify**: once a repo is big enough that Claude wanders, build the graph and enable its post-commit hook.
  First build costs tokens; not worth it on a near-empty repo.
- Bug-sized work: `/bugfix`. `/clear` after each.
