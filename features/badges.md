# badges

- Status: Built on local `feat/badges` branches (not merged or pushed)
- Surfaces: api | app
- Requirements: Roadmap #12 · `design/canvas/Badges.dc.html`

## Goal
Give every explorer an honest, release-forward catalogue of achievements and let them choose four earned badges
for their profile. Badges have no XP or gem rewards.

## Contract
- `GET /v1/badges` returns the complete catalogue, grouped totals, capped progress, earned timestamps and showcase.
  Guests receive the catalogue with zero progress.
- `PUT /v1/me/badges/showcase` accepts 0–4 unique earned keys in display order.
- `GET /v1/users/:username/badges` returns only the public profile's showcase.
- Awards are evaluated lazily on catalogue reads and showcase saves; they are idempotent and never revoked.
- `GameConfig badges.config.startAt` is the release cutoff, falling back to `2026-10-30T00:00:00.000Z`.

## Catalogue
64 badges: 15 Places + 12 Regions + 8 Seasons + 10 Social + 19 Milestones. The canvas named 45; the approved
Milestones group supplies the remaining 19 using facts the product already records. Names remain English proper
nouns in uz/ru/en; descriptions are localized agent-drafted copy. Eleven supplied PNGs are mapped; remaining
catalogue entries use a code-native locked/star fallback.

## Verification
API catalogue/service unit tests cover group totals, stable keys, English titles, release cutoff, progress,
awarding and showcase rules. The full API check is green, including PostgreSQL e2e. App renders loading, error,
guest, locked/progress, earned and four-pick states. iOS has not been built.
