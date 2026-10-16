# Setup (M0, done once by hand)

## Already prepared (2026-10-16)
- `irbis/` plain folder with four sibling git repos (`main` branch, nothing pushed).
- `irbis-docs`: CLAUDE.md, PROJECT.md, ROADMAP.md, STATUS.md, ADR-001..003, spec template,
  `/feature` + `/bugfix` commands, agents `api-dev`, `web-dev`, `app-dev` (sonnet), `reviewer` (opus).
- Hooks: PreToolUse blocks `.env*`, key files, `node_modules`/build dirs; Stop runs `npm run check`
  in every repo with changes (blocks once, then lets Claude report).
- Each code repo: short CLAUDE.md + `.claude/settings.json` (same deny rules + its own Stop hook).
- User-level (global): plugin `andrej-karpathy-skills`, MCP `context7` (current framework docs).

## Launch
```bash
cd ~/work/irbis/irbis-docs && ./scripts/start.sh
```
(`.claude/settings.json` also lists the three repos in `additionalDirectories`, so plain `claude` works too.)

## Remaining by-hand steps, in order
Generators refuse non-empty folders, so scaffold into a temp dir and copy over
(keep the existing `CLAUDE.md` and `.claude/`), or move those two aside and back.

1. **API**: `npx @nestjs/cli new irbis-api --package-manager npm --strict --skip-git`
   then add `@nestjs/swagger`, `prisma`, `@prisma/client`, `class-validator`, `class-transformer`, `@nestjs/config`.
   Add `scripts/export-openapi.ts` + `"openapi:export"`. Global JWT guard + `@Public()`, ValidationPipe, exception filter.
2. **Web**: `npx create-next-app@latest irbis-web --ts --app --src-dir --eslint --use-npm`
   then `@tanstack/react-query`, `orval` (dev). `orval.config.ts`: input `../irbis-api/openapi.json`,
   output `src/api/generated`, client `react-query`, mutator `src/api/mutator.ts`. Script `"gen:api": "orval"`.
3. **App**: `npx create-expo-app@latest irbis-app` (default template = Expo Router + TS),
   then same orval setup, `expo-secure-store`, `@tanstack/react-query`.
4. **`npm run check` in all three** — quiet, failures only, e.g.
   ```json
   "lint": "eslint . --quiet",
   "typecheck": "tsc --noEmit --pretty false",
   "test:ci": "vitest run --reporter=dot --silent",
   "slop": "! grep -rnE 'TODO|FIXME|@ts-ignore|eslint-disable|\\bmock' src --include='*.ts' --include='*.tsx' --exclude-dir=__tests__ --exclude='*.spec.*' --exclude='*.test.*' --exclude-dir=generated",
   "check": "npm run -s lint && npm run -s typecheck && npm run -s test:ci && npm run -s slop"
   ```
   (Jest in the API: `jest --silent --reporters=summary`.) ESLint: `@typescript-eslint/no-explicit-any: error`,
   `ban-ts-comment: error`, `eslint-comments/no-use` (or `--no-inline-config`), `eslint-plugin-boundaries`
   for `features/*` isolation; dependency-cruiser in the API to keep Prisma inside repositories.
5. **`.env.example`** in each repo with variable names only. Fill the real `.env` yourself; never paste values into chat.
6. **Pin versions** you actually installed into `PROJECT.md`; review and set ADR-001..003 to Accepted.
7. **Design**: tokens in `src/theme/tokens.ts` (web + app), 2–3 reference screens in `design/`.
8. **Reference feature** `health` end to end by hand (API endpoint → openapi → gen:api → web + app screen with all states).
   Every later feature copies this pattern.

## Later (not day one)
- **Graphify**: once a repo is big enough that Claude wanders, build the graph and enable its post-commit hook.
  First build costs tokens; not worth it on a near-empty repo.
- Bug-sized work: `/bugfix`. Feature-sized: `/feature`. `/clear` after each.
