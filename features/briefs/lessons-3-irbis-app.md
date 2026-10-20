# Brief lessons-3-irbis-app — Quiz play, sounds, lesson complete

- Spec: features/lessons.md · ACs in this slice: AC5, AC6 (mid-lesson + practice), AC7 (screen + local record + cache)
- Repo / branch: irbis-app · `feat/lessons` · Depends on: lessons-2-irbis-app (committed)

## Files
- Touch: `src/features/lessons/screens/QuizScreen.tsx` (replace slice-2 stub), `LessonCompleteScreen.tsx`,
  components (OptionButton, AnswerSheet, ProgressBar, QuitDialog, CompanionReaction), `quizMachine.ts` (pure state),
  `completionsStore.ts` (MMKV), `lessonCache.ts`, `sounds.ts`, `src/assets/sounds/` (copy the 3 m4a from
  `../irbis-docs/design/media/lessons/`), `src/assets/svg/companionFoxCheering.ts` (from
  `../irbis-docs/design/media/lessons/companion-fox-cheering.svg`), navigation types/routes, `lessons.json` ×3, tests.
- Read: `../irbis-docs/design/media/lessons/LAYOUT.md` § Quiz, `src/shared/components/levels/CompanionArt.tsx`,
  `Mascot.tsx` (`pandaCheering`), `src/shared/utils/haptics.ts`, slice-2 `heartsStore.ts` / `catalogStore.ts`.

## First (owner Q16)
- In `src/app/__tests__/auth/shell.test.tsx` ("AC1: Lessons and Community show the same empty state") remove
  only `lessons` from the loop; Community keeps its ComingSoon assertion. Commit separately: `test(auth): lessons tab
  is no longer coming soon (owner Q16)`. Tests live in `src/app/__tests__/lessons/` (boundaries), as slice 2 did.

## Behaviour
- AC5 — `useLessonsGet(lessonId)`; on success save the lesson to `lessonCache` (MMKV, by id); offline / error →
  cached copy, else "Connect to the internet to open this lesson" + Retry. Layout per LAYOUT.md § Quiz. Questions in
  admin order, options not shuffled. Progress = questions answered right / total. Chip = tier title · lesson title.
  Image (if any): RN `Image`, hidden on load error. Hint bubble only when `hint` exists (companion still shown).
  - Check (disabled until a pick) → correct: sheet "Nicely done!" + explanation, `haptics.success`, correct sound,
    companion cheering (fox L3 = new svg, panda L1 = `pandaCheering`, others = neutral `CompanionArt` + Reanimated bounce).
  - Wrong: sheet "Not quite — you lost a heart" + "Correct answer:" + correct option text + (wrongExplanation ??
    explanation), `haptics.error`, wrong sound, `heartsStore.loseHeart()`, broken-heart overlay, neutral companion.
  - Wrong questions are queued and re-asked after the last question until answered right (each wrong costs a heart).
  - Record every attempt `{ questionId, optionIndex }` in order.
  - Close X → QuitDialog "Quit lesson?" / "Your progress in this lesson is lost." / Quit · Keep learning.
  - Speaker toggle (MMKV `lessons.muted`, default on). Sounds: `react-native-audio-api` — load the 3 clips once,
    iOS audio session category `ambient` (respects the silent switch, mixes with music); never throw on audio errors
    (log via the app logger, keep playing silently). Check the 0.13 API in Context7.
- AC6 — Practice mode = lesson already done (server progress ∪ local completions): no heart loss, wrong sheet title
  "Not quite", header shows a "Practice" chip instead of hearts. New lesson: hearts reach 0 → OutOfHeartsSheet
  (slice 2) → back to hub; nothing recorded; QA `lesson_failed`.
- AC7 (screen) — after the last correct answer → LessonCompleteScreen: cheering companion + Reanimated burst
  (placeholder), "Lesson complete!", XP line: practice → "Practice — no XP"; else perfect (0 wrong) → `+xpPerfect XP`
  + "No hearts lost!", else `+xpFirst XP` (values from catalog `config`); "Correct first try: x / total"; hearts left;
  goal ring (slice-2 GoalRing, counting this one); Continue → hub. Lesson-complete sound. Guests also see "Sign up to
  keep your XP" button → existing log-in prompt sheet (find it in `src/features/auth`). New (non-practice) lesson:
  `completionsStore.add({ lessonId, completedAt: now ISO, attempts, perfect, synced: false })` and make slice-2
  `localCompletions()` read this store. Sending to the server is slice 4.

## Copy (`lessons.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| quiz.check | Check | Проверить | Tekshirish |
| quiz.correct | Nicely done! | Отлично! | Zo'r! |
| quiz.wrong | Not quite — you lost a heart | Не совсем — минус одно сердце | Unchalik emas — bitta yurak ketdi |
| quiz.wrongPractice | Not quite | Не совсем | Unchalik emas |
| quiz.correctAnswer | Correct answer: | Правильный ответ: | To'g'ri javob: |
| quiz.continue | Continue | Продолжить | Davom etish |
| quiz.gotIt | Got it | Понятно | Tushunarli |
| quiz.practice | Practice | Практика | Mashq |
| quiz.mute / unmute (a11y) | Sound off / Sound on | Выключить звук / Включить звук | Ovozni o'chirish / Ovozni yoqish |
| quiz.close (a11y) | Close lesson | Закрыть урок | Darsni yopish |
| quiz.progressA11y | Question %{n} of %{total} | Вопрос %{n} из %{total} | %{total} tadan %{n}-savol |
| quiz.quitTitle | Quit lesson? | Выйти из урока? | Darsdan chiqasizmi? |
| quiz.quitBody | Your progress in this lesson is lost. | Прогресс в этом уроке пропадёт. | Bu darsdagi natijangiz saqlanmaydi. |
| quiz.quit / keep | Quit / Keep learning | Выйти / Продолжить урок | Chiqish / Darsni davom ettirish |
| quiz.notCached | Connect to the internet to open this lesson | Подключитесь к интернету, чтобы открыть урок | Darsni ochish uchun internetga ulaning |
| complete.title | Lesson complete! | Урок пройден! | Dars tugadi! |
| complete.xp | +%{count} XP | +%{count} XP | +%{count} XP |
| complete.perfect | No hearts lost! | Ни одного сердца не потеряно! | Birorta ham yurak yo'qolmadi! |
| complete.practice | Practice — no XP | Практика — без XP | Mashq — XP berilmaydi |
| complete.firstTry | Correct first try: %{n} / %{total} | С первого раза: %{n} из %{total} | Birinchi urinishda: %{total} tadan %{n} |
| complete.hearts | Hearts left: %{count} | Осталось сердец: %{count} | Qolgan yuraklar: %{count} |
| complete.signup | Sign up to keep your XP | Зарегистрируйтесь, чтобы сохранить XP | XP saqlanishi uchun ro'yxatdan o'ting |

## testIDs · QA events
`quiz.close`, `quiz.progress`, `quiz.hearts`, `quiz.mute`, `quiz.option.<i>`, `quiz.check`, `quiz.sheet.correct`,
`quiz.sheet.wrong`, `quiz.continue`, `quiz.quit.confirm`, `lesson.complete`, `lesson.complete.xp`,
`lesson.complete.continue`, `lesson.complete.signup` · `lesson_started { lessonId, practice, hearts }`,
`lesson_answer { questionId, correct, hearts, retry }`, `lesson_failed { lessonId }`,
`lesson_completed { lessonId, practice, perfect, xp }`

## Approved packages
`react-native-audio-api@0.13.6` (owner Q12; peer `react-native-worklets` already installed — don't add others)

## Done when
- [ ] tests: quizMachine (re-ask, attempts, 0 hearts → fail, practice no heart loss); screen correct/wrong sheets;
  complete screen XP lines + local record; sounds mocked at the module boundary only. `npm run check` green (paste),
  Android build compiles (`cd android && ./gradlew assembleDebug -q` or the repo's build script), committed.
- [ ] Reply ≤ 10 lines.
