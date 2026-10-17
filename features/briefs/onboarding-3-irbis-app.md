# Brief onboarding-3-irbis-app — Experience, Interests, Companion reveal

- Spec: features/onboarding.md · ACs in this slice: AC4, AC5, AC6
- Repo / branch: irbis-app · `feat/onboarding`
- Depends on: onboarding-2-irbis-app (committed on the branch)

## Files
- Touch: `src/features/onboarding/` (screens Experience, Interests, Companion; `onboardingStore.ts` gets
  experience + interests; Language Continue → Experience) · `src/shared/i18n/{en,ru,uz}/onboarding.json` ·
  `src/assets/svg/` (new SVG string modules, same style as `irbisDefault.ts`) · `src/shared/components/Mascot.tsx`
  (add kind `pandaCheering`) · `src/shared/storage/index.ts` (keys).
- Art source (copy, convert to the `.ts` SvgXml pattern): `/Users/sardor/work/irbis/irbis-docs/design/media/onboarding/`
  — `onb3-trail.svg` `onb3-lake.svg` `onb3-peak.svg` `boot.svg` (if present) `interest-*.svg` `panda-cheering.svg`
  `companion-l2..l7.svg` `backpack-placeholder.svg`. Interest circle colours: Peaks #1CB0A8, Caves #7B61FF,
  Lakes #4CA9FF, Camping #3DAA5C, Trails #FF9F1C (put them in tokens if design.md lacks them — check first).
- Read for patterns: the slice-2 screens + `OnboardingHeader` + `Motion.tsx`, `src/shared/components/{Checkbox,
  Pressable,AppButton}.tsx`, `src/shared/utils/haptics.ts`, `design.md` tokens are already in `src/shared/` tokens.

## Behaviour
- AC4 — Experience (header step 2): Irbis default + bubble; radiogroup tiles Beginner (trail art, 1 boot),
  Weekend hiker (lake, 2 boots), Experienced (peak, 4 boots) — boots shown as N of 4 filled; none preselected;
  Continue disabled until one chosen; selection haptic. Orange info card with the quiz text, not pressable.
  Choice saved in the store (MMKV key `onboarding.experience`) on Continue.
- AC5 — Interests (step 3): Irbis excited + bubble; 2-col grid of toggle tiles (aria-pressed, checkbox corner),
  Trails full-width last; none preselected; counter "%{count} selected · …" updates live; Continue disabled at 0;
  saved (MMKV `onboarding.interests`, JSON array of ids in canonical order peaks,caves,lakes,camping,trails) on Continue.
- AC6 — Companion (no header; Android back → Interests): sunburst + confetti, eyebrow, title, panda cheering 270 on
  a green ellipse, level pill `1` · Wanderer · trait, body, six companion silhouettes (L2–L7, 40 px, tinted black at
  18 % opacity, a11y group "Locked companions"), `Let's go!` → end onboarding `via: 'finish'` with experience +
  interestsCount. On entry: Motion `onb5-reveal` with fallback = placeholder Reanimated sequence (backpack placeholder
  scales/shakes 3× over 600 ms, fades; panda springs in; 12 confetti rects fall for 800 ms), `haptics.success()`;
  Motion `irbis-clap` small in the corner with Irbis excited fallback. Reduced motion → static final frame.
- `onboarding_step` on each focus; `onboarding_end { via:'finish', experience, interestsCount }`.
- ✕ on steps 2–3 must NOT save experience/interests (clear any unsaved state).

## Copy (namespace `onboarding`)
| key | en | ru | uz |
|---|---|---|---|
| experience.bubble | How much hiking have you done? | Какой у тебя опыт походов? | Piyoda sayohatda tajribang qanday? |
| experience.beginner.title / .sub | Beginner / New to the mountains — short, easy walks | Новичок / Горы в новинку — короткие лёгкие прогулки | Yangi boshlovchi / Tog‘lar men uchun yangi — qisqa, oson sayrlar |
| experience.weekend.title / .sub | Weekend hiker / A few trails a season, day hikes up to 15 km | Хожу по выходным / Несколько маршрутов за сезон, однодневки до 15 км | Dam olish kunlari sayyohi / Mavsumda bir necha yo‘l, 15 km gacha bir kunlik sayrlar |
| experience.experienced.title / .sub | Experienced / Multi-day treks, scrambles, high passes | Опытный / Многодневные походы, скалы, высокие перевалы | Tajribali / Ko‘p kunlik yurishlar, qoyalar, baland dovonlar |
| experience.boots (a11y) | Difficulty %{n} of 4 | Сложность %{n} из 4 | Qiyinlik: %{n} / 4 |
| experience.quizCard | Everyone starts as a Wanderer. Experienced? Pass a short safety quiz to unlock harder places sooner. | Все начинают как Странник. Есть опыт? Пройди короткий тест по безопасности, чтобы быстрее открыть сложные места. | Hamma Sayyoh bo‘lib boshlaydi. Tajribalimisan? Qiyinroq joylarni tezroq ochish uchun xavfsizlik bo‘yicha qisqa testdan o‘t. |
| interests.bubble | What do you want to discover? Pick as many as you like. | Что хочешь открыть? Выбирай сколько угодно. | Nimalarni kashf qilmoqchisan? Xohlagancha tanla. |
| interests.peaks/caves/lakes/camping/trails | Peaks / Caves / Lakes / Camping / Trails | Вершины / Пещеры / Озёра / Кемпинг / Тропы | Cho‘qqilar / G‘orlar / Ko‘llar / Kemping / So‘qmoqlar |
| interests.count (plural) | one/other: %{count} selected | one: Выбрано %{count} · few/many/other: Выбрано %{count} | %{count} ta tanlandi |
| interests.hint | Your weekly path mixes these with safe options for the season. | Маршрут недели смешает их с безопасными вариантами по сезону. | Haftalik yo‘nalishing ularni mavsumga mos xavfsiz variantlar bilan aralashtiradi. |
| companion.eyebrow | Your starting companion | Твой первый спутник | Ilk hamrohing |
| companion.title | Meet Bao, your panda cub! | Знакомься: Бао, твой детёныш панды! | Tanish bo‘l: Bao, sening panda bolachang! |
| companion.level / .trait | Wanderer / clumsy & cozy | Странник / неуклюжий и уютный | Sayyoh / beo‘xshov va yoqimtoy |
| companion.body | Bao grows as you learn safety skills and check in at real places. Six more forms are waiting. | Бао растёт, когда ты учишь правила безопасности и отмечаешься в реальных местах. Впереди ещё шесть форм. | Bao sen xavfsizlikni o‘rganib, haqiqiy joylarda belgilanganingda o‘sadi. Yana oltita ko‘rinish kutmoqda. |
| companion.locked (a11y) | Locked companions | Закрытые спутники | Yopiq hamrohlar |
| companion.letsGo | Let's go! | Поехали! | Ketdik! |
Long ru/uz text wraps; buttons never truncate. Light + dark via tokens.

## testIDs · QA events
`onboarding.exp-{beginner|weekend|experienced}` `onboarding.interest-{peaks|caves|lakes|camping|trails}`
`onboarding.interests-count` `onboarding.continue` `onboarding.companion` `onboarding.lets-go` ·
`onboarding_step { step }` `onboarding_end { via, experience, interestsCount }`

## Approved packages
none (lottie-react-native already added in slice 2)

## Done when
- [ ] tests for AC4–AC6 (Continue disabled/enabled, saved values, ✕ saves nothing, Let's go ends + flag),
  `npm run check` green, committed; reply ≤10 lines with commit hash + check tail
