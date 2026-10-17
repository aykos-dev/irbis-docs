# Brief places-2-irbis-app — Place screen + level card

- Spec: features/places.md · ACs in this slice: AC7, AC8
- Repo / branch: irbis-app · `feat/places` (create from main)
- Depends on: places-1-irbis-api (pull `../irbis-api/openapi.json` via `npm run gen:api`)

## Files
- Touch: `src/features/places/` (new: `screens/PlaceScreen.tsx`, `components/` (LevelCard, SeasonBar, TypePill,
  DifficultyBoots, PlaceHero), `placeTypes.ts` (type → colour token, icon, illustration, i18n key),
  `formatDistance.ts`, `__tests__/`) · `src/app/navigation/types.ts` + `RootNavigator.tsx` (stack route
  `Place { id: string }` above the tabs) · `linking.ts` (`irbis://place/<id>`) · `src/assets/svg/placeCave.ts`
  (from `../irbis-docs/design/media/places/cave.svg`), `placeWaterfall.ts` + `placeCanyon.ts` (placeholders, same
  390×240 style, labelled placeholder in a comment) · `src/shared/components/Icon.tsx` (add waterfall + canyon glyphs if
  icons live there) · `src/shared/i18n/{en,ru,uz}/places.json` (+ register the namespace)
- Read for patterns (don't change): `src/features/onboarding/screens/ExperienceScreen.tsx` (SVG art, boots),
  `src/shared/components/{Screen,AppText,Skeleton,ErrorState,OfflineBanner,StatusChip}.tsx`, `src/shared/api/query.ts`,
  `src/assets/svg/onb3Peak.ts` + `onb3Lake.ts` (reuse for peak/lake heroes), `docs/architecture.md`,
  `../irbis-docs/design/design.md` (tokens: peak teal, lake blue, cave purple, camping green, trail orange)

## Behaviour
- AC7 — `useGetV1PlacesId` (generated name may differ — use the generated hook) with device/fallback coords passed
  in from navigation params if present (Explore passes `lat/lng` when it has them; deep link has none → API fallback).
  Layout per canvas `Place`/`PlaceDark`: hero = type illustration (no "1 / 48" counter); type pill colour + icon +
  label; name = `name[locale] ?? name.uz`; region line only if non-null; stat tiles Elevation "{n} m" and distance
  (formatDistance: < 10 km one decimal, else whole km, locale digits) with label "From you"/"From Tashkent" by
  `origin`; "Difficulty {d}/5" with 5 boots (d filled); LevelCard (AC8); description section only if
  `description[locale] ?? description.uz` non-null (plain text, keep paragraphs); SeasonBar when `season.length===12`:
  12 cells, initials, today's month (Asia/Tashkent) outlined + "Today: {month}", legend Best/Possible/Closed —
  else "Season not set yet"; hazards as chips (icon + label) or "Hazards not set yet". Nothing else from the canvas
  (conditions, weather, ratings, reports, trails, badges, verification, discoverer, Start adventure).
  Header back → previous screen. States: skeleton, ErrorState + retry, offline = cached data or offline message,
  404 → EmptyState "This place isn't available" + back.
- AC8 — `viewer.qualifies` → "Requires" / "Level {n} · {name}" / "or higher" + green check "You qualify"; else lock
  icon + same lines + "Reach Level {n} to go here". Level names by `requiredLevel` from i18n `levels.<n>`.
- QA event `place_viewed { slug, requiredLevel, qualifies }` once per successful load.

## Copy (`places` namespace; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| type.peak … canyon | Peak · Lake · Cave · Camping · Trail · Waterfall · Canyon | Пик · Озеро · Пещера · Кемпинг · Тропа · Водопад · Каньон | Cho‘qqi · Ko‘l · G‘or · Lager · So‘qmoq · Sharshara · Kanyon |
| elevation / elevationValue | Elevation / {{n}} m | Высота / {{n}} м | Balandlik / {{n}} m |
| distanceKm / fromYou / fromTashkent | {{d}} km / From you / From Tashkent | {{d}} км / От вас / От Ташкента | {{d}} km / Sizdan / Toshkentdan |
| difficulty | Difficulty {{d}}/5 | Сложность {{d}}/5 | Qiyinlik {{d}}/5 |
| level.requires / level.line / level.orHigher | Requires / Level {{n}} · {{name}} / or higher | Требуется / Уровень {{n}} · {{name}} / или выше | Talab / {{n}}-daraja · {{name}} / yoki undan yuqori |
| level.qualify / level.locked | You qualify / Reach Level {{n}} to go here | Вам доступно / Достигните уровня {{n}}, чтобы пойти сюда | Sizga ochiq / Bu yerga borish uchun {{n}}-darajaga yeting |
| levels.1 … 7 | Wanderer, Burrower, Pathfinder, Ridge Walker, Mountain Guardian, Sky Watcher, Snow Legend | Странник, Землекоп, Следопыт, Хребтоход, Страж гор, Небесный дозорный, Снежная легенда | Sayyoh, Qazuvchi, Izquvar, Tizma yo‘lovchisi, Tog‘ posboni, Osmon kuzatuvchisi, Qor afsonasi |
| about | About | Описание | Tavsif |
| season.title / season.today | Best season / Today: {{month}} | Лучший сезон / Сегодня: {{month}} | Eng yaxshi mavsum / Bugun: {{month}} |
| season.best / possible / closed | Best / Possible / Closed | Лучше всего / Возможно / Закрыто | Eng yaxshi / Mumkin / Yopiq |
| season.months | J F M A M J J A S O N D | Я Ф М А М И И А С О Н Д | Y F M A M I I A S O N D |
| season.empty | Season not set yet | Сезон пока не указан | Mavsum hali belgilanmagan |
| hazards.title / hazards.empty | Hazards / Hazards not set yet | Опасности / Опасности пока не указаны | Xavflar / Xavflar hali belgilanmagan |
| hazard.avalanche … road | Avalanche · Flood · Mudslide · Heat · Road | Лавина · Паводок · Сель · Жара · Дорога | Ko‘chki · Toshqin · Sel · Issiq · Yo‘l |
| notFound | This place isn't available | Это место недоступно | Bu joy mavjud emas |

Month name for "Today:" via `Intl.DateTimeFormat(locale, { month: 'long', timeZone: 'Asia/Tashkent' })`.

## testIDs · QA events
`place.screen`, `place.back`, `place.name`, `place.type`, `place.elevation`, `place.distance`, `place.difficulty`,
`place.level-card`, `place.level-qualify`, `place.level-locked`, `place.description`, `place.season`,
`place.season-empty`, `place.hazards`, `place.hazards-empty` · `place_viewed { slug, requiredLevel, qualifies }`

## Approved packages
none

## Done when
- [ ] tests: qualify vs locked card, season bar vs empty, distance format + locale name fallback; `npm run check` green
- [ ] committed on `feat/places`; reply ≤ 10 lines
