# lessons-admin

- Status: Draft
- Surfaces: api | web (app: none — lesson play is `lessons`, next)
- Related ADRs: ADR-002, ADR-003, ADR-005 (object storage, new)
- Requirements: Product Overview § Lessons (tiers, multiple-choice cards with hearts), § Levels (tier gates), § XP ·
  Screens: `design/canvas/LessonsHub`, `Quiz`, `QuizCorrect`, `QuizWrong` (content shape only; admin has no design,
  built from `design/design.md`) · `design/canvas-rules.md` (a) Progression, (b) 5–6
- Builds on: `levels` (GameConfig `levels.table`, tier keys "1","2","3","4","first-aid","5", level engine),
  `auth` (admin role, `@Roles`), `conditions` (admin controller + web admin page patterns).
- Branch: `feat/lessons-admin` from main in irbis-api and irbis-web.

## Goal
Admins write the safety lessons in the web panel: tiers → lessons → multiple-choice questions in uz/ru/en, with an
optional picture per question, and publish them. Only published lessons will be served to the app (`lessons`).
Level tier gates now count the tier's published lessons. The database starts with 6 tiers and 18 Claude-drafted
draft lessons for the owner to review.

## API (all `@Roles('admin')`, under `/v1/admin`)
| Method | Path | Request | Response | Errors |
|---|---|---|---|---|
| GET | /lesson-tiers | — | `{ items: AdminTier[] }` (by `order`) | — |
| POST | /lesson-tiers | `{ key, title: L10n, colour }` | `AdminTier` | TIER_KEY_TAKEN 409, VALIDATION_FAILED |
| PATCH | /lesson-tiers/{id} | `{ title?, colour? }` | `AdminTier` | TIER_NOT_FOUND 404 |
| POST | /lesson-tiers/reorder | `{ ids: string[] }` (all tiers) | `{ items }` | VALIDATION_FAILED |
| DELETE | /lesson-tiers/{id} | — | 204 | TIER_NOT_FOUND, TIER_NOT_EMPTY 409 |
| GET | /lesson-tiers/{id}/lessons | — | `{ items: AdminLessonSummary[] }` (by `order`) | TIER_NOT_FOUND |
| POST | /lesson-tiers/{id}/lessons/reorder | `{ ids }` | `{ items }` | TIER_NOT_FOUND, VALIDATION_FAILED |
| POST | /lessons | `{ tierId, title: L10n, icon }` | `AdminLesson` (draft, 0 questions) | TIER_NOT_FOUND |
| GET | /lessons/{id} | — | `AdminLesson` | LESSON_NOT_FOUND 404 |
| PUT | /lessons/{id} | `{ title, icon, questions: QuestionInput[] }` (whole lesson) | `AdminLesson` | LESSON_NOT_FOUND, VALIDATION_FAILED, LESSON_NOT_PUBLISHABLE 422 (when published) |
| POST | /lessons/{id}/publish | — | `AdminLesson` | LESSON_NOT_PUBLISHABLE 422 (`fieldErrors`) |
| POST | /lessons/{id}/unpublish | — | `AdminLesson` | — |
| DELETE | /lessons/{id} | — | 204 | LESSON_PUBLISHED 409 (unpublish first) |
| POST | /lesson-images | multipart `file` | `{ key, url, width, height }` | IMAGE_TYPE 415, IMAGE_TOO_LARGE 413 |

`L10n` = `{ uz, ru, en }` strings. `AdminTier` = `{ id, key, title, colour, order, lessonCount, publishedCount }`.
`AdminLessonSummary` = `{ id, title, icon, order, status: draft|published, questionCount, publishedAt, updatedAt }`.
`AdminLesson` = summary + `tierId`, `questions: { id, order, prompt: L10n, hint: L10n|null, options: L10n[] (2–4),
correctIndex, explanation: L10n, wrongExplanation: L10n|null, image: { key, url }|null }[]`.
`QuestionInput` = the same without `id`/`order` (array order = question order; `image` = `{ key }`).
`icon` ∈ `compass leaf padlock cloud paw first-aid mountain waves avalanche bolt`.

## Data model changes
New migration `lessons_admin_init`.
- `LessonTier { id, key String @unique (immutable, ^[a-z0-9-]{1,20}$), title Json, colour String, order Int, timestamps }`
- `enum LessonStatus { draft published }` · `Lesson { id, tierId → LessonTier (RESTRICT), title Json, icon String,
  order Int, status @default(draft), publishedAt?, timestamps }` index `(tierId, status, order)`
- `LessonQuestion { id, lessonId → Lesson (CASCADE), order Int, prompt Json, hint Json?, options Json, correctIndex Int,
  explanation Json, wrongExplanation Json?, imageKey String? }` `@@unique([lessonId, order])`
- Seed (idempotent, by `key`): tiers `1` Trail Basics · `2` Mountain Ready · `3` Ridge Skills · `4` Snow & Scrambles ·
  `first-aid` First aid · `5` Leadership (uz/ru/en titles, canvas colours). Draft lessons: separate seed (AC8).
- Env (ADR-005): `S3_ENDPOINT`, `S3_REGION`, `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`,
  `S3_FORCE_PATH_STYLE`, `S3_PUBLIC_BASE_URL` (placeholders in `.env.example`); MinIO + bucket-init in docker-compose.

## Acceptance criteria
- **AC1** — Tiers: an admin lists, creates, renames/recolours, reorders and deletes tiers. `key` is unique and can
  never change (level gates use it); deleting a tier with any lesson → 409 TIER_NOT_EMPTY. Non-admin → 403,
  no token → 401. Migration seeds the 6 tiers above in that order.
- **AC2** — Lessons: create a draft in a tier (title L10n + icon), list a tier's lessons with status and question
  count, reorder them (`ids` must be exactly that tier's lessons), read one, replace it whole with `PUT` (title, icon,
  0–15 questions). Draft saves accept empty locale strings; structure is always checked: 2–4 options,
  `0 ≤ correctIndex < options.length`, ≤ 15 questions, text ≤ 300 chars (option ≤ 120) → else VALIDATION_FAILED
  with `fieldErrors` paths like `questions.3.options.1.ru`.
- **AC3** — Publish rules: `publish` succeeds only when title and every prompt, option and explanation has non-blank
  uz, ru and en (hint / wrongExplanation optional, but if one locale is set all three must be), and the lesson has
  5–15 questions; otherwise 422 LESSON_NOT_PUBLISHABLE listing every failing path in `fieldErrors`. `PUT` on a
  published lesson applies the same rules (stays published, or 422 and nothing saved). `unpublish` → draft;
  `publishedAt` keeps the first publish time. Deleting a published lesson → 409 LESSON_PUBLISHED.
- **AC4** — Images (ADR-005): `POST /lesson-images` accepts one JPEG/PNG/WebP ≤ 2 MB (else 415 / 413), re-encodes it
  without metadata (EXIF/GPS gone) with the longest side ≤ 1600 px, stores it at `lessons/<uuid>.<ext>` and returns
  `{ key, url, width, height }`. A question saves `image.key` only if the key starts with `lessons/` and exists in
  the bucket (else VALIDATION_FAILED). Responses carry `url = S3_PUBLIC_BASE_URL/key`. Storage errors → 503
  STORAGE_UNAVAILABLE (logged with requestId, no secret values).
- **AC5** — Level gates: for `levels.table` rows with lesson kind `tier`, `required` = the number of **published**
  lessons in the tier with that key; kind `all` = all published lessons; kind `count` (L2 "any 2") stays the config
  number. A gate whose tier has 0 published lessons is **not met** (nobody passes an empty safety tier) and shows
  `required: 0`. `GET /v1/levels` and `GET /v1/me/level` show the computed numbers. Unpublishing never lowers a
  level (levels never go down). The level engine still reads lesson facts only; no client change.
- **AC6** — Web Lessons pages (admin nav "Lessons"): Tiers page — table (order, colour chip, title in the admin's UI
  locale, key, lessons, published) with create / edit dialog (key, uz/ru/en title, colour), move up / down, delete
  (disabled with a tooltip when not empty). Tier page — its lessons (order, icon, title, status badge Draft /
  Published, questions, updated), "New lesson" dialog (uz/ru/en title + icon picker of the 10 glyphs), move up / down,
  row → editor. States: skeleton, empty ("No lessons yet — create the first one"), error + retry.
- **AC7** — Web lesson editor: title uz/ru/en + icon; a question list (add, remove with confirm, move up / down,
  max 15) where each question has prompt, hint, 2–4 options with a "correct" radio, explanation, wrong-answer
  explanation — each a uz / ru / en input group with a per-locale "missing" marker — and an optional image (upload,
  preview, remove; 415/413 shown inline). Buttons Save draft · Publish · Unpublish · Delete (drafts only, confirm).
  Server `fieldErrors` are shown on the exact inputs and as a count "N fields missing to publish"; leaving with
  unsaved changes asks to confirm. All UI copy in next-intl uz/ru/en.
- **AC8** — Draft content seed: a separate idempotent seed (`npm run db:seed`, skipped when the tier already has
  lessons) adds 3 draft lessons per tier = 18 lessons × 10 questions, uz/ru/en, from the doc topics (Tier 1:
  Navigation basics, Leave no trace, Gear essentials · 2: Weather signs, Wildlife & plants, First aid I · 3: Altitude &
  health, Route finding, River crossing · 4: Avalanche awareness, Scrambling, Storms on ridges · First aid: Bleeding &
  wounds, Sprains & fractures, Hypothermia & heat · Leadership: Planning a group trip, Turn-around decisions, Group
  emergencies). Content is Central Asia specific, factual and marked as Claude drafts for owner review; all stay
  draft (nothing reaches users until the owner publishes). Includes the canvas altitude-sickness question.

### QA events
- none (no app change)

### testIDs (web, `data-testid`)
`lessons.tiers.table`, `lessons.tiers.new`, `lessons.tier.row.<key>`, `lessons.tier.up|down|delete`,
`lessons.list.table`, `lessons.list.new`, `lessons.lesson.row.<id>`, `lessons.editor`, `lessons.editor.title.<loc>`,
`lessons.editor.icon`, `lessons.editor.q.<n>`, `lessons.editor.q.<n>.correct.<i>`, `lessons.editor.q.<n>.image`,
`lessons.editor.add-question`, `lessons.editor.save`, `lessons.editor.publish`, `lessons.editor.unpublish`,
`lessons.editor.delete`, `lessons.editor.missing-count`

### Required UI states (every touched client)
- [x] Loading (skeleton tables, editor skeleton)
- [x] Empty (no tiers / no lessons / no questions)
- [x] Error (message + retry; field errors inline)
- [ ] Offline — admin web: generic error state is enough
- [ ] Permissions denied — non-admin uses the existing admin gate
- [x] Unsaved-changes guard, disabled buttons while saving, press states
- [x] Design tokens + `src/components/ui` (shadcn) primitives only

## Media
`design/media/lessons-admin/MEDIA.md` — glyphs and tier colours exist on canvas (final); question images are uploaded
content.

## Waivers
- none

## Out of scope
- App LessonsHub / Quiz play, public lesson endpoints, hearts, XP for lessons, guest merge, offline (→ `lessons`).
- Version history / scheduled publishing / per-locale publishing · bulk import/export · cleaning orphan images ·
  moving a lesson to another tier · user photo uploads.

## Assumptions
- Q1 (owner, 2026-10-20): admin editor is needed; split → `lessons-admin` first (api + web), then `lessons` (app play).
- Q2 (owner, 2026-10-20): structure Tier → Lesson → Question; any number of lessons per tier.
- Q3 (owner, 2026-10-20): single-choice questions with optional images; publish needs uz + ru + en.
- Q4 (owner, 2026-10-20): a tier gate = all published lessons of that tier (L7 "all" = all published).
- Q5 (owner, 2026-10-20): seed the 6 tiers + Claude-drafted draft lessons for review; tier 5 named "Leadership".
- Q6 (owner, 2026-10-20): images in MinIO (S3 compatible) → ADR-005; upload through the api (my choice: simpler
  than presigned, strips metadata in one place).
- Q7 (Claude, 2026-10-20): 5–15 questions to publish (canvas lesson = 10); 3 drafts per tier = the doc's named topics.
- Q8 (Claude, 2026-10-20): an empty published tier blocks its level gate rather than passing it.

## Open questions
- none
