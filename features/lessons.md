# lessons

- Status: Approved (2026-10-20)
- Surfaces: api | app (web: no change — content is edited in `lessons-admin`)
- Related ADRs: ADR-001 (guest-first, guest merge), ADR-002, ADR-003, ADR-005 (question images)
- Requirements: Product Overview § Lessons (tiers, multiple-choice cards with hearts), § XP ("Safety lesson 10–15"),
  § Accounts ("lesson progress stays on the phone and moves into the account") · Screens: `design/canvas/LessonsHub`,
  `Quiz`, `QuizCorrect`, `QuizWrong`, `LevelUp` (one line) · `design/canvas-rules.md` (a) hearts, daily goal
- Builds on: `lessons-admin` (LessonTier / Lesson / LessonQuestion, published lessons, `StorageService.publicUrl`),
  `levels` (`award` source `lesson`, `recordFact` kind `lesson` + tier, GameConfigService, LevelUp screen),
  `auth` (guest-merge registry + `guestStore`, `@Public()` optional auth).
- Branch: `feat/lessons` from main in irbis-api and irbis-app (lessons-admin fast-forwarded into main first, owner Q14).

## Goal
Anyone (guest or signed in) opens the Lessons tab, picks any published lesson in any tier, and plays it as
multiple-choice cards with 5 daily hearts. A finished lesson earns 10 XP (15 with no heart lost) once, counts toward
the level's lesson gates and today's goal of 3, works offline once opened, and guests keep their progress on sign-up.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/lessons | `@Public()` (user optional) | — | `LessonCatalog` | — |
| GET | /v1/lessons/{id} | `@Public()` | — | `PublicLesson` | LESSON_NOT_FOUND 404 (unknown or draft) |
| POST | /v1/me/lesson-completions | user | `CompletionInput` | `CompletionResult` | LESSON_NOT_FOUND 404, VALIDATION_FAILED 400 |
| POST | /v1/me/guest-merge | user | existing + `lessons?: { completions: CompletionInput[] }` (≤ 200) | existing | existing |

- `LessonCatalog` = `{ config: { heartsPerDay, xpFirst, xpPerfect, dailyGoal }, tiers: { key, title: L10n, colour,
  order, lessons: { id, title: L10n, icon, order, questionCount, updatedAt }[] }[] (published only, tiers without
  published lessons left out), progress: { completedLessonIds: string[], doneToday: number } | null }` (null for guests).
- `PublicLesson` = `{ id, tierKey, title, icon, updatedAt, questions: { id, order, prompt, hint|null, options: L10n[],
  correctIndex, explanation, wrongExplanation|null, image: { url, width?, height? }|null }[] }`.
- `CompletionInput` = `{ lessonId, completedAt (ISO), attempts: { questionId, optionIndex }[] (in answer order, ≤ 75) }`.
- `CompletionResult` = `{ firstCompletion, perfect, xpAwarded, doneToday, dailyGoal, levelUps }`.

## Data model changes
Migration `lessons_completions`.
- `LessonCompletion { id, userId → User (CASCADE), lessonId → Lesson (CASCADE), completedAt, wrongCount Int,
  perfect Boolean, xp Int, createdAt }` `@@unique([userId, lessonId])` (first completion only), index `(userId, completedAt)`.
- GameConfig key `lessons.config` = `{ heartsPerDay: 5, xpFirst: 10, xpPerfect: 15, dailyGoal: 3 }` (zod, seed row).

## Acceptance criteria
- **AC1** — Catalog: `GET /v1/lessons` returns published lessons only, grouped by tier (`order`, then lesson `order`),
  full uz/ru/en texts, `config` from `lessons.config`, and for a signed-in user `progress` (completed lesson ids,
  `doneToday` = first completions with `completedAt` in today's Asia/Tashkent day). `GET /v1/lessons/{id}` returns a
  published lesson with all questions, `correctIndex` and image URLs; a draft or unknown id → 404 LESSON_NOT_FOUND.
- **AC2** — Completion: `POST /v1/me/lesson-completions` grades `attempts` on the server. Valid when every question of
  the lesson has a final correct attempt and wrong attempts ≤ `heartsPerDay − 1` (4); else 400 VALIDATION_FAILED.
  First completion → `LessonCompletion` row, `award(source lesson, refId lessonId)` of `xpPerfect` (15) if 0 wrong
  else `xpFirst` (10), `recordFact(kind lesson, tier key)`; later ones → `firstCompletion:false`, 0 XP, nothing
  written (idempotent). If the attempts name question ids the lesson no longer has (edited after the phone cached
  it), the completion is still accepted as not perfect (10 XP). `completedAt` older than 7 days or in the future is
  replaced by now. Draft/unknown lesson → 404. No token → 401.
- **AC3** — Guest merge: handler key `lessons` takes `completions` and runs each through AC2 (invalid ones skipped,
  not failing the merge); safe to run twice (no double XP). Level gates count merged lessons.
- **AC4** — LessonsHub (Lessons tab replaces ComingSoon): header with hearts left today (heart + number); daily goal
  ring `doneToday / dailyGoal` with "Daily goal · 3-minute lessons" and a line ("%{n} more to reach today's goal" /
  "Goal reached — nice work!"); tiers as on canvas (tier colour, "Tier N" label, title, `done / total`, "Done" when all
  done), lesson nodes with icon glyph, title, done tick; the first not-done lesson (tier order) gets "START". All
  tiers open (Q5, canvas Tier 4 lock dropped). No streak flame (→ `streaks`). Done = server progress ∪ local
  completions. States: skeleton, empty ("Lessons are on their way" + Irbis), error + retry, offline = cached catalog
  with the offline banner (no cache → offline message).
- **AC5** — Quiz: header close (X), progress bar (questions answered right / total), hearts; tier · lesson label,
  prompt, optional image, hint bubble with the companion, 2–4 options A–D, Check (disabled until a pick). Correct →
  green sheet "Nicely done!" + explanation + Continue, success haptic + correct sound, cheering companion. Wrong →
  red sheet "Not quite — you lost a heart" + "Correct answer:" + wrongExplanation (else explanation) + Got it, error
  haptic + wrong sound, −1 heart. Wrong questions are asked again after the last one until answered right (Q8).
  X → confirm "Quit lesson? Your progress in it is lost." (hearts lost stay lost). Speaker toggle in the header mutes
  sounds, remembered on the phone; sounds also respect the silent switch (Q13).
- **AC6** — Hearts (on the phone, Q9): 5 per Asia/Tashkent day (`heartsPerDay`), back to 5 at 00:00 Tashkent; shared
  by guest and signed-in use on that phone. A new lesson needs ≥ 1 heart to start, else "Out of hearts — back at
  midnight" (sleepy Irbis, time left). Reaching 0 mid-lesson ends it: same sheet, lesson not counted, no XP (Q7).
  A finished lesson can be replayed as practice: no heart cost, no XP, not in the daily goal (Q10), label "Practice".
- **AC7** — Lesson complete + sync: screen with cheering companion, "Lesson complete!", XP (+15 "No hearts lost!",
  +10, or "Practice — no XP"), correct first try x / total, hearts left, daily goal ring, Continue → hub; guests also
  see "Sign up to keep your XP" (→ log-in prompt sheet). Signed in: the first completion is POSTed; offline or on a
  network error it is queued on the phone and sent on reconnect / app start (shown done meanwhile, XP shown from
  `config`). Guests: first completions stay on the phone and go in `guest-merge` (`lessons`) on sign-up / log-in.
  Opened lessons (and their images when online) are cached for offline replay.
- **AC8** — LevelUp line (Q11): replace the canvas "Tier N lessons are open" idea with "Next: %{tier} lessons count
  toward Level %{n}" when the next level's lesson gate is a tier gate (tier title from the cached catalog, else
  "Tier %{tier}"); no line for count / all gates or at Level 7.

### QA events (app, dev/staging builds)
- `lesson_started { lessonId, practice, hearts }` · `lesson_answer { questionId, correct, hearts, retry }`
- `lesson_failed { lessonId }` (0 hearts) · `lesson_completed { lessonId, practice, perfect, xp }`
- `lesson_sync { sent, queued }` · `hearts_reset { hearts }`

### testIDs (app)
`lessons.hub`, `lessons.hearts`, `lessons.goal`, `lessons.tier.<key>`, `lessons.lesson.<id>`, `lessons.start`,
`lessons.empty`, `lessons.error.retry`, `quiz.close`, `quiz.progress`, `quiz.hearts`, `quiz.mute`, `quiz.option.<i>`,
`quiz.check`, `quiz.sheet.correct`, `quiz.sheet.wrong`, `quiz.continue`, `quiz.quit.confirm`, `quiz.outofhearts`,
`lesson.complete`, `lesson.complete.xp`, `lesson.complete.continue`, `lesson.complete.signup`, `levelup.nextTier`.
Debug link (dev/staging): `irbis://debug/lessons/hearts/<0-5>` sets today's hearts.

### Required UI states (every touched client)
- [x] Loading (hub skeleton, quiz loading)
- [x] Empty (no published lessons)
- [x] Error (message + retry; completion errors → queued, never lost)
- [x] Offline (cached hub + opened lessons; not-opened lesson → "Connect to the internet to open this lesson")
- [ ] Permissions denied — none needed
- [x] Safe areas, haptics, press states; options/buttons wrap in ru/uz (never truncate)
- [x] Design tokens and `src/shared/components` primitives only; light + dark

## Media
`design/media/lessons/MEDIA.md`: glyphs, tier colours, hearts, chrome = canvas (final). Fox cheering
(`companion-fox-cheering.svg`) from canvas; other companions' cheering / concerned poses and the completion burst are
placeholders (neutral pose + Reanimated) — STATUS known issue (Q11). Sounds: 3 Kenney CC0 clips (m4a), Q12–Q13.

## Waivers
- none

## Out of scope
- Streak flame / streak line (→ `streaks`), gems or Plus heart refills, hearts synced across devices, Bu qayer?,
  lesson badges, onboarding safety quiz (→ `onboarding-quiz`), web changes, re-grading old completions after edits,
  lesson-level evolution art.

## Assumptions
- Q1 (owner, 2026-10-20): hearts = daily pool of 5 per Asia/Tashkent day, refilled at 00:00; a wrong answer costs one.
- Q2 (owner, 2026-10-20): at 0 hearts new lessons lock until midnight; finished lessons replay as practice (no heart
  cost, no XP); starting a new lesson needs ≥ 1 heart.
- Q3 (owner, 2026-10-20): XP 10 first completion, 15 with no heart lost, server config; correct sheet "Nicely done!"
  without XP; XP on the lesson-complete screen.
- Q4 (owner, 2026-10-20): guests take lessons; completions stay on the phone, sent via guest-merge; opened lessons
  cached; offline completions queued.
- Q5 (owner, 2026-10-20): all tiers open, any order (canvas Tier 4 "Unlocks when you reach Level 4" dropped).
- Q6 (owner, 2026-10-20): daily goal = lessons finished today (Tashkent) / 3 (server config); streak with `streaks`.
- Q7 (owner, 2026-10-20): 0 hearts mid-lesson ends it — "Out of hearts", not counted, no XP.
- Q8 (owner, 2026-10-20): wrong questions are re-asked at the end until right; each wrong costs a heart.
- Q9 (owner, 2026-10-20): hearts live on the phone; the server grades submitted answers and decides 10 vs 15 XP.
- Q10 (owner, 2026-10-20): lesson-complete = full summary; daily goal counts first completions only (no practice).
- Q11 (owner, 2026-10-20): LevelUp line names the next tier gate; missing poses/celebration = placeholders now.
- Q12 (owner, 2026-10-20): sound + haptics; package `react-native-audio-api` approved.
- Q13 (owner, 2026-10-20): Kenney CC0 sounds; in-lesson mute toggle, remembered; silent mode respected.
- Q14 (owner, 2026-10-20): merge lessons-admin into main first, branch `feat/lessons` from main (done: api 30a5c39,
  web 3eba4ed).
- Q15 (Claude, 2026-10-20): question order as the admin set it, options not shuffled; hub has no "you" tier marker or
  level names (tiers are not tied to the player's level any more).
- Q16 (owner, 2026-10-20): `src/app/__tests__/auth/shell.test.tsx` "AC1: Lessons and Community show the same
  empty state" — remove `lessons` from its loop (Community keeps the ComingSoon assertion); nothing else changed.

## Open questions
- none
