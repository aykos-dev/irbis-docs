# Brief lessons-2-irbis-app — LessonsHub + daily hearts

- Spec: features/lessons.md · ACs in this slice: AC4, AC6 (hearts store + hub gate; mid-lesson part is slice 3)
- Repo / branch: irbis-app · `feat/lessons` (exists, from main)
- Depends on: lessons-1-irbis-api committed on irbis-api `feat/lessons` (run `npm run gen:api`)

## Files
- Touch: `src/features/lessons/` (new: `screens/LessonsHubScreen.tsx`, `components/` (TierCard, LessonNode,
  GoalRing, HeartsCount, LessonGlyph, OutOfHeartsSheet), `heartsStore.ts`, `catalogStore.ts`, `__tests__/`) ·
  `src/app/navigation/TabNavigator.tsx` (Lessons tab → hub, replaces ComingSoon) + `types.ts` · `linking.ts` + debug
  feature (link `irbis://debug/lessons/hearts/<0-5>`, dev/staging only) · `src/shared/i18n/{en,ru,uz}/lessons.json`
  + `src/shared/i18n/index.ts` · `src/shared/api/generated/` via `npm run gen:api` only.
- Read for patterns (don't change): `src/features/levels/` (screens, hooks, i18n use), `src/shared/storage/index.ts`
  (MMKV), `src/shared/hooks/useNetworkStatus.ts`, `src/shared/components/OfflineBanner.tsx`, `Mascot.tsx`,
  `src/features/debug/` (debug links), `../irbis-docs/design/media/lessons/LAYOUT.md` (all sizes, colours, glyph paths).

## Behaviour
- AC4 — Hub = generated `useLessonsList` (operationId `lessonsList`). Layout exactly per LAYOUT.md § LessonsHub.
  - Hearts in header = today's hearts from `heartsStore` (below).
  - Goal ring: `doneToday` = server `progress.doneToday` (signed in) + local first completions dated today (Tashkent)
    not yet in `completedLessonIds`; target `config.dailyGoal`. Line: "n more" plural, or "Goal reached".
  - Done set = `progress.completedLessonIds` ∪ local completions (slice 3 writes them; read via a `catalogStore`
    selector `localCompletions()` that returns [] for now — keep the API small: `{ lessonId, completedAt }[]`).
  - Tier caption: keys "1"–"5" → "Tier N"; `first-aid` → "First aid". Pill "done / total" or ✓ "Done".
  - START on the first not-done lesson in tier order. All nodes tappable (no locks). Tap → navigate `Quiz`
    `{ lessonId }` (add the route with a stub screen that only shows the lesson title — slice 3 builds it).
  - Starting a NOT done lesson with 0 hearts → OutOfHeartsSheet instead of navigating. Done lessons always open.
  - Text in the user's locale from L10n `{uz,ru,en}`.
  - States: skeleton; empty (no tiers) → Irbis default + "Lessons are on their way"; error → message + Retry;
    offline → last catalog snapshot from MMKV (`catalogStore`, saved on every successful fetch) + OfflineBanner;
    offline and no snapshot → offline message.
- AC6 — `heartsStore` (MMKV key `lessons.hearts` = `{ day: 'YYYY-MM-DD' Tashkent, hearts }`): reading on a new
  Tashkent day resets to `config.heartsPerDay` (default 5 until a catalog is loaded); `loseHeart()` (min 0),
  `hearts()`, `msUntilReset()`; shared by guest and signed-in use; not cleared on sign-out. Re-render the hub when the
  day flips while open (check on focus / app foreground). OutOfHeartsSheet: Mascot `sleepy`, title, body with time
  left "hh:mm", button OK. Debug link sets today's hearts (dev/staging only). QA events `hearts_reset { hearts }`.

## Copy (`lessons.json`)
| key | en | ru | uz |
|---|---|---|---|
| hub.title | Lessons | Уроки | Darslar |
| hub.heartsA11y | %{count} hearts left | Осталось сердец: %{count} | %{count} ta yurak qoldi |
| goal.title | Daily goal · 3-minute lessons | Цель дня · уроки по 3 минуты | Kunlik maqsad · 3 daqiqalik darslar |
| goal.more (one/few/many/other as levels.json) | %{count} more lesson(s) to reach today's goal | Ещё %{count} урок/урока/уроков до цели дня | Bugungi maqsadga yana %{count} ta dars |
| goal.done | Goal reached — nice work! | Цель дня выполнена — молодец! | Maqsad bajarildi — barakalla! |
| tier.caption | Tier %{n} | Ступень %{n} | %{n}-bosqich |
| tier.firstAid | First aid | Первая помощь | Birinchi yordam |
| tier.done | Done | Готово | Tayyor |
| node.start | START | НАЧАТЬ | BOSHLASH |
| empty | Lessons are on their way | Уроки скоро появятся | Darslar tez orada |
| error | Couldn't load lessons | Не удалось загрузить уроки | Darslarni yuklab bo'lmadi |
| retry | Try again | Повторить | Qayta urinish |
| offline | You're offline. Lessons will load when you're back online. | Нет сети. Уроки загрузятся, когда появится интернет. | Internet yo'q. Darslar internet qaytganda yuklanadi. |
| hearts.outTitle | Out of hearts — back at midnight | Сердца закончились — вернутся в полночь | Yuraklar tugadi — yarim tunda qaytadi |
| hearts.outBody | New hearts in %{time}. You can still replay lessons you've finished. | Новые сердца через %{time}. Пройденные уроки можно повторять. | Yangi yuraklar %{time} dan keyin. Tugatgan darslaringizni takrorlashingiz mumkin. |
| hearts.ok | OK | Понятно | Tushunarli |

## testIDs · QA events
`lessons.hub`, `lessons.hearts`, `lessons.goal`, `lessons.tier.<key>`, `lessons.lesson.<id>`, `lessons.start`,
`lessons.empty`, `lessons.error.retry`, `quiz.outofhearts` · `hearts_reset { hearts }`

## Approved packages
none

## Done when
- [ ] tests: hub renders tiers/done/START; empty + error + offline snapshot; hearts day reset + 0-hearts sheet
  (1–3 per AC); `npm run check` green (paste output); committed on `feat/lessons`. Don't edit existing tests — report.
- [ ] Reply ≤ 10 lines.
