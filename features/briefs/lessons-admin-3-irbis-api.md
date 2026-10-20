# Brief lessons-admin-3-irbis-api — draft lesson content seed

- Spec: features/lessons-admin.md · ACs in this slice: AC8
- Repo / branch: irbis-api · `feat/lessons-admin`
- Depends on: brief lessons-admin-1-irbis-api (models + tiers)

## Files
- Touch: `prisma/seed/lessons.data.ts` (new, typed data) · `prisma/seed/seed.ts` (call it) · a small rules check
  `prisma/seed/lesson-seed.rules.ts` + spec (pattern: `place-seed.rules.ts`)
- Read for patterns: `prisma/seed/seed.ts`, `place-seed.rules.ts`, `places.data.ts`

## Behaviour
- AC8 — 18 lessons, 3 per tier, all `status: draft`, each with exactly 10 questions, uz (Latin) / ru / en filled for
  title, prompt, 4 options, explanation and wrongExplanation; hint on ~half the questions (all 3 locales). Icons from
  `compass leaf padlock cloud paw first-aid mountain waves avalanche bolt`. Topics:
  - 1: Navigation basics (compass) · Leave no trace (leaf) · Gear essentials (padlock)
  - 2: Weather signs (cloud) · Wildlife & plants (paw) · First aid I (first-aid)
  - 3: Altitude & health (mountain) · Route finding (compass) · River crossing (waves)
  - 4: Avalanche awareness (avalanche) · Scrambling (mountain) · Storms on ridges (bolt)
  - first-aid: Bleeding & wounds · Sprains & fractures · Hypothermia & heat (first-aid)
  - 5: Planning a group trip · Turn-around decisions · Group emergencies (compass / mountain / bolt)
- Content: accurate, conservative outdoor-safety guidance for Uzbekistan / Central Asia (Chimgan, Beldersay, Chatkal,
  Pskem, Fann; snake/ tick / bear awareness; emergency number 112; spring river melt; summer heat; winter avalanche).
  One correct option, three plausible wrong ones; correct option position varied. Short sentences, friendly, never
  guilt. Altitude & health includes the canvas question exactly: prompt "What should you do if you notice signs of
  altitude sickness?", hint "Headache, nausea, dizziness… think safety first!", explanation "Stop climbing and rest.
  If symptoms don't improve within a few hours — or get worse — descend at least 300–500 m. Never go higher with
  symptoms.", wrongExplanation "Stop ascending and rest; descend if symptoms persist. Rushing higher makes altitude
  sickness worse."
- Uzbek in Latin script with ʻ (U+02BB) for oʻ/gʻ. No real people's names or phone numbers.
- Idempotent: for each tier, skip if it already has any lesson. A file header comment says "Claude draft — owner
  review before publishing".
- Rules check (spec): 18 lessons, 10 questions each, all locales non-blank, ≤300/≤120 chars, correctIndex valid —
  i.e. every lesson would pass the AC3 publish rules.

## Approved packages
none

## Done when
- [ ] rules spec green, `npm run check` green (paste output), `npm run db:seed` runs twice on a local DB without
  duplicates (or say why it could not run), committed
- [ ] reply ≤10 lines
