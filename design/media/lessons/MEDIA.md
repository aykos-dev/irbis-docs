# Media — lessons

App screens: LessonsHub, Quiz, QuizCorrect, QuizWrong (canvas) + lesson-complete and out-of-hearts (no board).
Question images are admin-uploaded content (lessons-admin), not design media.

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| Lesson icon glyphs ×10 | Lesson node icons (compass, leaf, padlock, cloud, paw, first-aid, mountain, waves, avalanche, bolt) | LessonsHub nodes | inline SVG paths from canvas LessonsHub | exists on canvas · final (lessons-admin) |
| Tier colours ×6 | Tier header / node colour | LessonsHub | tokens from canvas | exists on canvas · final (lessons-admin) |
| Heart + broken heart | Hearts counter in header, wrong-answer state | LessonsHub, Quiz, QuizWrong | inline SVG from canvas | exists on canvas |
| Close (X), progress bar, check / cross marks, Done tick, lock | Quiz chrome, hub nodes | Quiz*, LessonsHub | inline SVG / views from canvas | exists on canvas |
| Companion neutral (current level) | Speech-bubble guide on the question | Quiz, QuizWrong | `CompanionArt` (levels) | exists in app |
| Companion cheering, per level (7) | Correct answer + lesson complete | QuizCorrect, lesson complete | SVG, ~120 px | panda (L1) exists in app; fox (L3) `companion-fox-cheering.svg` (from canvas); L2, L4–L7 placeholder: neutral + Reanimated bounce (owner Q11) |
| Companion concerned, per level (7) | Wrong answer (assets.md "concerned" pose) | QuizWrong | SVG, ~120 px | placeholder: neutral pose, as on canvas (owner Q11) |
| Irbis sleepy | Out of hearts — back at midnight | LessonsHub / Quiz out-of-hearts | SVG | exists in app (`Mascot kind="sleepy"`) |
| Lesson-complete celebration | Confetti / burst behind the companion | lesson complete | Lottie or Reanimated | placeholder OK: Reanimated burst (owner Q11) |
| `lesson-correct.m4a`, `lesson-wrong.m4a`, `lesson-complete.m4a` | Answer / complete sounds (Kenney Interface Sounds confirmation_002, error_006, confirmation_004, CC0 — `KENNEY-LICENSE.txt`), AAC 96k | Quiz, lesson complete | m4a, 6–8 KB | exists · CC0 (owner Q13); played with react-native-audio-api (Q12) |
