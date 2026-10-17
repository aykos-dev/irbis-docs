# Brief places-4-irbis-api-fix — review fix: seed idempotency test (AC1)

- Spec: features/places.md · AC1 · Repo / branch: irbis-api · `feat/places` (on 0f4c5ee)
- Files: Touch `test/places-seed.e2e-spec.ts` (new) and, only if needed to make the seed callable from a test,
  export the upsert loop from `prisma/seed/seed.ts` as a function taking a PrismaClient (no behaviour change).
  Read: `prisma/seed/seed.ts`, `test/places.e2e-spec.ts`, `test/setup/`.
- Behaviour: Testcontainers DB → run the real seed (all 71 rows from `places.data.ts`) twice → `place.count() === 71`
  after each run; spot-check one row (`qorangur-2941`: nameUz `Qorangur`, difficulty 3, requiredLevel 3, type peak).
- Approved packages: none. Do not edit existing tests.
- Done when: `npm run check` green, one commit `test(places): seed is idempotent against a real DB (AC1)`, reply ≤5 lines.
