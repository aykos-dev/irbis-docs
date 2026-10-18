# Brief levels-3-irbis-app — Level screen, Companions screen, entry points

- Spec: features/levels.md · ACs in this slice: AC5, AC6 (+ the AC8 entry points: Profile badge, Place level card)
- Repo / branch: irbis-app · `feat/levels` — create from `feat/conditions` (head 70998f6) (owner Q8)
- Depends on: levels-2-irbis-api (`openapi.json` on irbis-api `feat/levels` → `npm run gen:api`)

## Files
- Touch: `src/shared/components/levels/` (new, shared because auth Profile + places use it): `LevelFrame.tsx`
  (react-native-svg shape per level), `CompanionArt.tsx` (level → svg; `silhouette` prop = black at 35 %),
  `levelMeta.ts` (pure: per level frame shape, colour/dark/tint/text, i18n keys) · `src/assets/svg/` add full-colour
  `companionL2.ts`, `companionL4.ts`…`companionL7.ts` from `irbis-docs/design/media/onboarding/companion-l{2,4,5,6,7}.svg`
  (L1 `companionPanda.ts`, L3 `companionFox.ts` exist) · `src/features/levels/` (new): `screens/LevelScreen.tsx`,
  `screens/CompanionsScreen.tsx`, `hooks/useMyLevel.ts` (generated hook + MMKV `levels.lastMyLevel`),
  `hooks/useLevelDefs.ts` (generated `/v1/levels`, MMKV `levels.defs`), `formatRequirement.ts` (pure), `__tests__/` ·
  `src/shared/constants/colors.ts` (extend `levelColors` with dark/tint/text from the table below) · navigation:
  register `Level` + `Companions` routes in the root stack · `src/features/auth/screens/ProfileScreen.tsx:46-50`
  (badge: real companion + colour, `profile.companion-badge`, opens Level) ·
  `src/features/places/components/LevelCard.tsx` (pressable → Level, `place.level-card`) ·
  `src/shared/i18n/{en,ru,uz}/levels.json` (new)
- Read for patterns: `src/features/places/screens/PlaceScreen.tsx` (states, Skeleton/ErrorState/OfflineBanner),
  Explore MMKV cache (`explore.lastList`), the auth guest gate (how AccGate / Create account / Log in open),
  `onboarding/components/CompanionReveal.tsx`, design canvas values below. Reuse `places.levels.<n>` names.

## Level visuals (from canvas `Companions`)
| L | shape | color | dark | tint | text | boots |
|---|---|---|---|---|---|---|
| 1 | circle | #58B368 | #3E8E4D | #E4F5E7 | #2D6E3A | 1 |
| 2 | rounded square (r 44/184) | #C98B4E | #A06A33 | #F7EADB | #7A4E1F | 2 |
| 3 | shield `50% 0,100% 12%,100% 58%,50% 100%,0 58%,0 12%` | #F2802E | #C9601A | #FFE9D9 | #9A4510 | 3 |
| 4 | hexagon `25% 3%,75% 3%,100% 50%,75% 97%,25% 97%,0 50%` | #1CB0A8 | #0E8A83 | #DDF5F3 | #0C6E69 | 3 |
| 5 | octagon `30% 0,70% 0,100% 30%,100% 70%,70% 100%,30% 100%,0 70%,0 30%` | #4C7BD9 | #335FB8 | #E3ECFB | #2A4F9A | 4 |
| 6 | gem `50% 0,94% 20%,100% 62%,50% 100%,0 62%,6% 20%` | #7B61FF | #5B42DB | #ECE8FF | #4B33C4 | 4 |
| 7 | 24-point star (canvas `star` polygon) | #E5A800 | #B88600 | #FFF6D6 | #7A5800 | 5 |
Frame: outer shape `color` 210 px with a 6 px `dark` drop shadow, inner shape `tint` 184 px, art 160 px.
Requirement icons: XP bolt on #FFC800 (fill #FFC800 bar), lessons cross on #D93636 (bar #1CB0A8), boot on #8C5A33
(bar #F2802E). Dark mode: card/text tokens from design.md; level colours unchanged.

## Behaviour
- AC5 — Level (`level.screen`), header "Your level" + back. Logged in: `useMyLevel`. Frame (`level.frame`), pill
  (`level.pill`), name (`level.name`), since line (`level.since`, month from `reachedAt` in device TZ). If `next`:
  card "To reach Level {n} · {name}", rows `level.req-xp`, `level.req-lessons` (label by `lessons.kind`/`tier`:
  count → lessonsCount, tier "first-aid" → lessonsFirstAid, other tier → lessonsTier, all → lessonsAll),
  `level.req-checkins` + note, `level.req-spots` only when `verifiedSpots` non-null. Values "{current} / {required}"
  with locale thousands separator; bar width `min(current/required,1)`. Next-companion card (`level.next-companion`):
  next art as silhouette, "Next companion", "{name} · ???", "Unlocks {unlock}.". `next` null → `level.max` card.
  "See all companions" (`level.companions-link`). Button `level.continue` → Lessons tab. Guest: L1 + bars
  `0 / required` from `/v1/levels` L2 row; `level.guest-cta` card with `level.guest-signup` / `level.guest-login`
  (existing auth flow) instead of the button. Loading skeleton; error → ErrorState + `level.retry`; offline → cached
  data + OfflineBanner, none cached → offline message + retry. `level_viewed { level, guest }` once per open.
- AC6 — Companions (`companions.screen`): 7 cards (`companions.card.<n>`) — frame 120 px + art, "LEVEL N" pill,
  boots (`maxDifficulty` filled of 5, rest at 18 % opacity), name, "{animal} · {trait}", requirements line via
  `formatRequirement(def)` (L1 → companions.start), "Unlocks: {unlock}". Current level card has a "You" chip
  (`companions.you`) and a `color` border; levels above yours → silhouette art. Guest = level 1.
  `companions_viewed { level }`.

## Copy (namespace `levels`; ru/uz plurals via i18n-js `count`)
| key | en | ru | uz |
|---|---|---|---|
| title | Your level | Ваш уровень | Sizning darajangiz |
| pill | LEVEL %{n} | УРОВЕНЬ %{n} | %{n}-DARAJA |
| since | %{animal} · since %{month} %{year} | %{animal} · с %{month} %{year} | %{animal} · %{year}-yil %{month}dan beri |
| months (12, ru genitive) | January…December | января…декабря | yanvar…dekabr |
| animal.1–7 | Panda cub / Marmot / Fox / Ibex / Brown bear / Golden eagle / Snow leopard | Детёныш панды / Сурок / Лиса / Горный козёл / Бурый медведь / Беркут / Снежный барс | Panda bolasi / Sug‘ur / Tulki / Tog‘ echkisi / Qo‘ng‘ir ayiq / Burgut / Qor qoploni |
| trait.1–7 | clumsy & cozy / curious / clever / sure-footed / strong & protective / sharp-eyed / rare & respected | неуклюжий и уютный / любопытный / умная / уверенный на скалах / сильный и заботливый / зоркий / редкий и уважаемый | beo‘xshov va yoqimtoy / qiziquvchan / aqlli / qoyada ishonchli / kuchli va g‘amxo‘r / o‘tkir ko‘zli / noyob va hurmatli |
| unlock.1–7 | difficulty 1 places / difficulty 2 places / difficulty 3 and overnight trips / scrambles and high passes / difficulty 4 and leading group trips / verifying other explorers' spots / difficulty 5 and the Legend frame | места сложности 1 / места сложности 2 / сложность 3 и походы с ночёвкой / скрэмблинг и высокие перевалы / сложность 4 и ведение групповых походов / проверка мест других исследователей / сложность 5 и рамка Легенды | 1-qiyinlikdagi joylar / 2-qiyinlikdagi joylar / 3-qiyinlik va tunab qolinadigan sayohatlar / qoyaga tirmashish va baland dovonlar / 4-qiyinlik va guruh sayohatlarini boshqarish / boshqa sayyohlar joylarini tasdiqlash / 5-qiyinlik va Afsona ramkasi |
| toReach | To reach Level %{n} · %{name} | До уровня %{n} · %{name} | %{n}-darajaga yetish uchun · %{name} |
| req.xp | Earn XP | Наберите XP | XP to‘plang |
| req.lessonsCount / lessonsTier / lessonsFirstAid / lessonsAll | Safety lessons / Tier %{tier} safety lessons / First-aid safety lessons / All safety lessons | Уроки безопасности / Уроки безопасности, ступень %{tier} / Уроки первой помощи / Все уроки безопасности | Xavfsizlik darslari / %{tier}-bosqich xavfsizlik darslari / Birinchi yordam darslari / Barcha xavfsizlik darslari |
| req.checkIns / checkInsNote | Verified check-ins at difficulty %{d}+ / GPS check-in on site counts; photos alone don't. | Подтверждённые отметки на сложности %{d}+ / Засчитывается отметка по GPS на месте; одних фото мало. | %{d}+ qiyinlikda tasdiqlangan belgilar / Joyida GPS orqali belgilanish hisoblanadi; faqat suratlar hisoblanmaydi. |
| req.spots | Verified spots | Подтверждённые места | Tasdiqlangan joylar |
| next.cap / next.name / next.unlocks | Next companion / %{name} · ??? / Unlocks %{unlock}. | Следующий спутник / %{name} · ??? / Открывает: %{unlock}. | Keyingi hamroh / %{name} · ??? / Ochadi: %{unlock}. |
| max | You're a Snow Legend — the top level. | Вы — Снежная легенда, это высший уровень. | Siz Qor afsonasisiz — bu eng yuqori daraja. |
| continue / seeAll | Continue learning / See all companions | Продолжить обучение / Все спутники | O‘qishni davom ettirish / Barcha hamrohlar |
| guest.title | Create an account to earn XP and level up | Создайте аккаунт, чтобы получать XP и расти в уровне | XP yig‘ish va darajani oshirish uchun akkaunt yarating |
| companions.title / eyebrow / start / you / unlocks | Companions / Seven companions, one backpack / Where every explorer starts. / You / Unlocks: %{unlock} | Спутники / Семь спутников, один рюкзак / Отсюда начинает каждый исследователь. / Вы / Открывает: %{unlock} | Hamrohlar / Yetti hamroh, bitta ryukzak / Har bir sayyoh shu yerdan boshlaydi. / Siz / Ochadi: %{unlock} |
| fmt.lessonsCount (plural) / lessonsTier / lessonsFirstAid / lessonsAll | %{count} safety lessons / Tier %{tier} lessons / First-aid tier / all tiers | %{count} урок / урока / уроков безопасности · Уроки ступени %{tier} · Ступень первой помощи · все ступени | %{count} ta xavfsizlik darsi · %{tier}-bosqich darslari · Birinchi yordam bosqichi · barcha bosqichlar |
| fmt.checkIns (plural; minDifficulty 1) / checkInsAt (≥2) / spots | %{count} verified check-ins / %{count} check-ins at difficulty %{d}+ / %{count} verified spots | %{count} подтверждённая отметка/-ые отметки/-ых отметок · %{count} отметка/отметки/отметок на сложности %{d}+ · %{count} подтверждённое место/-ых места/-ых мест | %{count} ta tasdiqlangan belgi · %{d}+ qiyinlikda %{count} ta belgi · %{count} ta tasdiqlangan joy |
| fmt.xp / join | %{xp} XP / " · " | %{xp} XP / " · " | %{xp} XP / " · " |
| error / offline | Couldn't load your level / You're offline — level not loaded | Не удалось загрузить уровень / Нет сети — уровень не загружен | Darajani yuklab bo‘lmadi / Internet yo‘q — daraja yuklanmadi |
Guest buttons + "Try again": reuse the existing auth/common keys. uz apostrophe is ‘ (U+2018) as in existing files.

## Approved packages
none

## Done when
- [ ] tests: formatRequirement per kind/locale (ru plural); LevelScreen next/L7/guest states; Companions "You" +
  silhouettes; Profile badge shows level colour; `npm run check` green (output in summary), committed on `feat/levels`
