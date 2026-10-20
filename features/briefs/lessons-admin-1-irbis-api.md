# Brief lessons-admin-1-irbis-api — content model, tiers, lessons, publish

- Spec: features/lessons-admin.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-api · `feat/lessons-admin` (create from main)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` + new migration `lessons_admin_init` (models + tier seed rows in SQL or seed.ts,
  idempotent by `key`) · `src/features/lessons-admin/` (new: admin controller, service, repository, errors, dto/)
  · `src/app.module.ts` (register module) · `openapi.json` (export)
- Read for patterns (don't change): `src/features/conditions/admin-conditions.controller.ts`,
  `admin-conditions.service.ts`, `conditions.repository.ts` (LocalizedText Json), `conditions.errors.ts`,
  `src/common/decorators/roles.decorator.ts`, `prisma/seed/seed.ts`

## Data model (exact)
- `LessonTier { id uuid, key String @unique, title Json, colour String, order Int, createdAt, updatedAt }` table `lesson_tiers`
- `enum LessonStatus { draft published }`
- `Lesson { id, tierId → LessonTier onDelete Restrict, title Json, icon String, order Int, status LessonStatus @default(draft),
  publishedAt DateTime?, createdAt, updatedAt }` `@@index([tierId, status, order])` table `lessons`
- `LessonQuestion { id, lessonId → Lesson onDelete Cascade, order Int, prompt Json, hint Json?, options Json,
  correctIndex Int, explanation Json, wrongExplanation Json?, imageKey String? }` `@@unique([lessonId, order])` table `lesson_questions`
- Seed tiers (order 1–6, idempotent upsert by key, never overwrite admin edits):
  | key | en | ru | uz | colour |
  |---|---|---|---|---|
  | 1 | Trail Basics | Основы тропы | Yoʻl asoslari | #58CC02 |
  | 2 | Mountain Ready | Готов к горам | Togʻga tayyor | #1CB0A8 |
  | 3 | Ridge Skills | Навыки хребта | Tizma koʻnikmalari | #FF9600 |
  | 4 | Snow & Scrambles | Снег и скалы | Qor va qoyalar | #1899D6 |
  | first-aid | First aid | Первая помощь | Birinchi yordam | #FF4B4B |
  | 5 | Leadership | Лидерство | Yetakchilik | #8C5A33 |

## Behaviour
- AC1 — tiers: list (with `lessonCount`, `publishedCount`), create (`key` ^[a-z0-9-]{1,20}$, unique → 409
  TIER_KEY_TAKEN; `colour` #RRGGBB; appended last), PATCH title/colour only (key not accepted), reorder (`ids` must be
  exactly all tier ids → else VALIDATION_FAILED; orders become 1..n), delete (any lesson → 409 TIER_NOT_EMPTY).
- AC2 — lessons: POST draft (title L10n, icon in the 10 keys, appended last in tier); GET tier lessons; reorder (ids =
  exactly that tier's lessons); GET one; PUT whole lesson replaces questions in one transaction (array order = order).
  Draft structure checks: options 2–4, `0 ≤ correctIndex < options.length`, ≤ 15 questions, any L10n text ≤ 300
  chars (option ≤ 120), L10n objects must have uz/ru/en string keys (may be ""). `fieldErrors` paths like
  `questions.3.options.1.ru`, `title.uz`.
- AC3 — publish: title + every prompt/option/explanation non-blank in all 3 locales; hint/wrongExplanation null or
  all 3 non-blank; 5–15 questions → else 422 LESSON_NOT_PUBLISHABLE with every failing path. Sets status published,
  `publishedAt` only if null. PUT on a published lesson validates publish rules (422, nothing saved). Unpublish →
  draft. DELETE published → 409 LESSON_PUBLISHED; draft → 204.
- All routes `@Roles('admin')` under `/v1/admin`; 401 no token, 403 non-admin.
- Leave `image` handling for slice 2: accept `image: null` only in this slice (shape `{ key } | null` in DTO,
  non-null → VALIDATION_FAILED "images arrive in slice 2" is NOT acceptable — instead just store nothing and add a
  clear typed hook point in the service for slice 2 to validate keys).

## API
Exactly the table in the spec "API" section (lesson-tiers, lessons; not lesson-images). Error body per PROJECT.md.

## Tests (1–3 per AC)
- e2e: tier CRUD + key immutable + TIER_NOT_EMPTY; 403 for user role · lesson PUT validation paths · publish 422
  paths + success + PUT-on-published 422 + delete 409.

## Approved packages
none in this slice

## Done when
- [ ] tests above, `npm run check` green (paste output), `npm run openapi:export` committed, committed on the branch
- [ ] reply ≤10 lines: commits, endpoints, test count
