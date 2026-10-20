# Brief lessons-1-irbis-api — public lessons, completions, guest merge

- Spec: features/lessons.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-api · `feat/lessons` (exists, from main which now includes lessons-admin)
- Depends on: none

## Files
- Touch: `src/features/lessons/` (new: controller(s), service, repository, errors, dto, guest-merge handler,
  module) · `prisma/schema.prisma` + new migration `lessons_completions` · `src/features/levels/levels.constants.ts`,
  `game-config.schema.ts`, `game-config.service.ts` (add key `lessons.config` + getter) ·
  `prisma/seed/game-config.data.ts` (seed row) · `src/features/auth/dto/guest-merge.dto.ts` (add `lessons?`) ·
  `src/app.module.ts` (import module) · `openapi.json` (export) · tests under `test/` + unit specs.
- Read for patterns (don't change): `src/features/lessons-admin/` (models, L10n DTOs, image URL via
  `StorageService.publicUrl`), `src/features/levels/levels.service.ts` (`award` :92, `recordFact` :147),
  `src/features/auth/guest-merge/guest-merge.registry.ts` + `src/features/onboarding/onboarding-merge.handler.ts`,
  `src/common/decorators/public.decorator.ts` (optional user on public routes), `src/lib/dates.ts`
  (`startOfTashkentDay`), `test/levels-api.e2e-spec.ts` (e2e setup).

## Behaviour
- AC1 — `GET /v1/lessons` (`@Public()`): `{ config, tiers, progress }`.
  `config` = GameConfig `lessons.config` `{ heartsPerDay: 5, xpFirst: 10, xpPerfect: 15, dailyGoal: 3 }` (zod: ints ≥ 1,
  `xpPerfect ≥ xpFirst`). `tiers` = tiers by `order` that have ≥ 1 published lesson: `{ key, title: L10n, colour, order,
  lessons: { id, title, icon, order, questionCount, updatedAt }[] }` (published only, by `order`). `progress` = null for
  guests; signed in: `{ completedLessonIds, doneToday }` where `doneToday` = the user's `LessonCompletion` rows with
  `completedAt ≥ startOfTashkentDay(now)`.
  `GET /v1/lessons/:id` (`@Public()`): published lesson `{ id, tierKey, title, icon, updatedAt, questions: { id, order,
  prompt, hint, options, correctIndex, explanation, wrongExplanation, image: { url } | null }[] }` (by order). Draft /
  unknown / bad uuid → 404 `LESSON_NOT_FOUND`.
- AC2 — `POST /v1/me/lesson-completions` (user): body `{ lessonId (uuid), completedAt (ISO), attempts: { questionId
  (uuid), optionIndex (int 0–3) }[] (1–75) }`. Lesson must be published, else 404. Grading:
  - attempts whose `questionId` is in the lesson are graded against `correctIndex`; `wrong` = their wrong count.
  - Valid when every current question has ≥ 1 correct attempt AND `wrong ≤ heartsPerDay − 1`; else 400
    `VALIDATION_FAILED` (`fieldErrors.attempts`).
  - If any attempt names a question id not in the lesson (lesson edited after caching): skip the coverage check,
    accept, `perfect = false`.
  - `completedAt` in the future or older than 7 days → use now.
  - First completion (no row for userId+lessonId): in one flow create `LessonCompletion { completedAt, wrongCount,
    perfect, xp }`, `levels.award({ source: 'lesson', refId: lessonId, amount: perfect ? xpPerfect : xpFirst })`,
    `levels.recordFact({ kind: 'lesson', refId: lessonId, tier: tierKey })`. Unique-constraint race → treat as repeat.
  - Repeat: nothing written, `xpAwarded: 0`, `firstCompletion: false`.
  - Response `{ firstCompletion, perfect, xpAwarded, doneToday, dailyGoal, levelUps }` (`levelUps` from award result).
- AC3 — Guest merge handler key `lessons`, registered in `onModuleInit`. DTO `lessons?: { completions:
  CompletionInput[] (≤ 200) }`. Each completion runs the AC2 logic; invalid / unknown ones are skipped (logged without
  user data), never failing the merge. Running twice gives no extra XP.

## Data model
`LessonCompletion { id uuid, userId → User (CASCADE), lessonId → Lesson (CASCADE), completedAt, wrongCount Int, perfect
Boolean, xp Int, createdAt }` table `lesson_completions`, `@@unique([userId, lessonId])`, `@@index([userId, completedAt])`.
New migration only; GameConfig seed row idempotent.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| GET | /v1/lessons | — | LessonCatalog | — |
| GET | /v1/lessons/{id} | — | PublicLesson | LESSON_NOT_FOUND → 404 |
| POST | /v1/me/lesson-completions | CompletionInput | CompletionResult | LESSON_NOT_FOUND → 404, VALIDATION_FAILED → 400, 401 |

Swagger: tag `lessons`, operationIds `lessonsList`, `lessonsGet`, `lessonsComplete` (orval hook names derive from them).

## Tests (1–3 per AC)
- e2e AC1: guest gets published only (draft hidden) + `progress: null`; signed-in `doneToday` counts today only; 404 draft.
- e2e AC2: perfect → 15 XP + fact (gate count moves); 1 wrong → 10; repeat → 0, no second ledger row; missing
  correct answer / 5 wrongs → 400; unknown question id → accepted, 10 XP.
- e2e AC3: guest-merge with 2 completions → XP once; second merge → no new XP; invalid entry skipped.
- Existing tests: do not edit any. If one breaks, stop and report.

## Approved packages
none

## Done when
- [ ] tests above, `npm run check` green (paste output), `npm run openapi:export` committed, commits on `feat/lessons`
- [ ] Reply ≤ 10 lines: commits, endpoints, operationIds, anything not done
