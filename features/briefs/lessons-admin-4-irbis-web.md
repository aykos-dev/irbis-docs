# Brief lessons-admin-4-irbis-web — tiers page + tier lessons page

- Spec: features/lessons-admin.md · ACs in this slice: AC6
- Repo / branch: irbis-web · `feat/lessons-admin` (create from main)
- Depends on: api slices 1–2 on irbis-api `feat/lessons-admin` (run `npm run gen:api` against its openapi.json)

## Files
- Touch: `src/app/(admin)/lessons/page.tsx`, `src/app/(admin)/lessons/[tierId]/page.tsx` (new) ·
  `src/features/lessons-admin/` (components, hooks, schemas) · admin nav (add "Lessons" after "Conditions") ·
  `src/shared/i18n/messages/{en,ru,uz}.json` (namespace `lessonsAdmin`) · generated api (gen:api only)
- Read for patterns: `src/app/(admin)/conditions/page.tsx`, `src/features/conditions/components/conditions-list-view.tsx`,
  `end-dialog.tsx`, `write-errors.ts`, `schemas.ts`, `src/shared/components/`

## Behaviour (AC6)
- Tiers page: table columns Order · Colour (chip) · Title (admin UI locale) · Key · Lessons · Published; actions
  move up / down (calls reorder with the new full id list), Edit, Delete (disabled + tooltip "Remove its lessons
  first" when lessonCount > 0; confirm dialog otherwise). "New tier" dialog: key (validated ^[a-z0-9-]{1,20}$,
  disabled when editing), title uz/ru/en (required), colour (#RRGGBB input + swatch). 409 TIER_KEY_TAKEN → inline on key.
- Row click → tier page: header with tier title + colour; table Order · Icon · Title · Status badge (Draft grey /
  Published green) · Questions · Updated (Asia/Tashkent, dd.MM.yyyy HH:mm); up / down; "New lesson" dialog
  (title uz/ru/en + icon picker of 10 glyphs as buttons with aria-label) → on create navigate to
  `/lessons/[tierId]/[lessonId]` (editor comes in slice 5; route may show a stub with only a back link until then).
- States: skeleton table, empty ("No lessons yet — create the first one"), error + retry, buttons disabled while saving.
- Icon glyph set: create `src/features/lessons-admin/lesson-icons.tsx` with 10 simple inline SVGs keyed
  `compass leaf padlock cloud paw first-aid mountain waves avalanche bolt` (24 px, currentColor).

## Copy (namespace lessonsAdmin)
| key | en | ru | uz |
|---|---|---|---|
| nav | Lessons | Уроки | Darslar |
| tiers.title | Lesson tiers | Уровни уроков | Dars bosqichlari |
| tiers.new | New tier | Новый уровень | Yangi bosqich |
| tiers.deleteBlocked | Remove its lessons first | Сначала удалите уроки | Avval darslarni oʻchiring |
| lessons.new | New lesson | Новый урок | Yangi dars |
| lessons.empty | No lessons yet — create the first one | Уроков пока нет — создайте первый | Hozircha dars yoʻq — birinchisini yarating |
| status.draft | Draft | Черновик | Qoralama |
| status.published | Published | Опубликован | Eʼlon qilingan |
| keyTaken | This key is already used | Этот ключ уже занят | Bu kalit band |
Other labels (column headers, Edit, Delete, Save, Cancel, Move up/down, Retry) — write en/ru/uz in the same style.

## testIDs
`lessons.tiers.table`, `lessons.tiers.new`, `lessons.tier.row.<key>`, `lessons.tier.up`, `lessons.tier.down`,
`lessons.tier.delete`, `lessons.list.table`, `lessons.list.new`, `lessons.lesson.row.<id>`

## Approved packages
none (shadcn component files may be added via its CLI only if their deps are already installed; otherwise report)

## Done when
- [ ] 1–2 Vitest tests (tiers table + delete disabled; new lesson dialog validation), `npm run check` green (paste), committed
- [ ] reply ≤10 lines
