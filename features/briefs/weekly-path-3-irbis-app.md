# Brief weekly-path-3-irbis-app — Path screen: header, weather, nodes, states

- Spec: features/weekly-path.md · ACs in this slice: AC1 (client), AC2, AC6, AC7, AC8
- Repo / branch: irbis-app · `feat/weekly-path` (create from main)
- Depends on: weekly-path-1-irbis-api (run `npm run gen:api` against `../irbis-api/openapi.json` on its branch)

## Files
- Touch: `src/features/weekly-path/` (new: `screens/PathScreen.tsx`, `components/` (PathHeader, WeatherStrip,
  PathTrail, PathNode, NodePopover, ChestNode (static, progress only), HowBuiltSheet), `pathCache.ts`, `hooks/`,
  `__tests__/`) · `src/app/navigation/TabNavigator.tsx` (Path → PathScreen, replaces ComingSoon) ·
  `src/shared/i18n/{en,ru,uz}/path.json` + `src/shared/i18n/index.ts` · `src/shared/api/generated/` (gen:api only).
- Read for patterns (don't change): `../irbis-docs/design/media/weekly-path/LAYOUT.md` (sizes, colours, SVG paths,
  dark tints), `src/features/lessons/screens/LessonsHubScreen.tsx` (header, states, cache), `src/shared/components/`
  (StatusChip, Mascot `kind="worried"`, Skeleton, EmptyState, ErrorState, OfflineBanner, Sheet, Motion),
  `shared/components/conditions/weatherGlyph.tsx` + `reasonText.ts`, `features/places/placeTypes.ts`,
  `shared/components/levels/levelMeta.ts` + `CompanionArt.tsx`, `features/onboarding/onboardingStore.ts`
  (`getInterests()`), `shared/storage` (MMKV), `features/explore/screens/ExploreScreen.tsx:58` (navigate to Place).

## Behaviour
- AC1/AC2 — `usePathGet` (generated). Guests pass `interests` = `getInterests()` joined by commas (omit if empty).
  - Nodes render top→bottom on a winding line (LAYOUT.md), then the chest.
  - Each node shows a ring in the status colour plus a type glyph, and a chip below with icon + label:
    - go → "Go · {Sat}"
    - caution → "Caution · {reason}" (`reasonText`)
    - not_now → "Not now"
    - seasonal_lock → "Opens in {Month}"
    - null → no chip
  - Dark mode uses the brighter ring tints from LAYOUT.md.
  - Tapping a node: medium haptic, a scale bounce (Motion), and a popover with the name, the chip and "Open place" →
    `navigate('Place', { id })`. The popover closes on outside tap.
  - A not_now node shows `Mascot kind="worried"` beside it, with a gentle sway and a rain loop (Reanimated,
    placeholder). Reduce-motion turns both off.
- AC6 — Header:
  - `CompanionArt` for the user's level (guests L1), plus the XP total + bolt for accounts only (from the response
    `level` + existing `/v1/me/level` hook if already cached; no new endpoint).
  - Title `path.title`, subtitle `path.subtitle` with `{month}` (`path.months.1..12`), `{levelName}` (levelMeta) and
    `{season}` (`path.seasons.*`: Dec–Feb winter, Mar–May spring, Jun–Aug summer, Sep–Nov autumn).
  - An info button (`path.info`) opens HowBuiltSheet.
  - ChestNode in this slice is static: closed chest + `path.chest.progress`. Tapping it does nothing yet (slice 4).
- AC7 — WeatherStrip shows the API `weather.days` (Fri / Sat / Sun labels), each with a glyph (`weatherGlyph`), max
  °C and wind km/h, plus `path.weather.credit`. Empty days → the strip is hidden.
- AC8 — States:
  - Loading: Skeleton.
  - `nodes.length === 0`: EmptyState with the worried mascot, `path.empty.*`, and a button → Explore tab.
  - Error: ErrorState + Retry.
  - Offline: the last successful response for the current Tashkent month from `pathCache` (MMKV key
    `path.cache.<YYYY-MM>`, guests too) + OfflineBanner. No cache → the offline EmptyState.
  - Pull to refresh refetches.
  - On tab focus, if the cached `month` ≠ the current Tashkent month, refetch.

## Copy (namespace `path`)
| key | en | ru | uz |
|---|---|---|---|
| title | This Month's Path | Путь месяца | Oy yo'li |
| subtitle | %{month} · built for %{levelName}, %{season} | %{month} · для уровня %{levelName}, %{season} | %{month} · %{levelName} uchun, %{season} |
| status.go | Go · %{day} | Можно · %{day} | Boring · %{day} |
| status.caution | Caution · %{reason} | Осторожно · %{reason} | Ehtiyot · %{reason} |
| status.notNow | Not now | Не сейчас | Hozir emas |
| status.opens | Opens in %{month} | Откроется в %{month} | %{month}da ochiladi |
| days.fri / sat / sun | Fri / Sat / Sun | Пт / Сб / Вс | Ju / Sh / Ya |
| openPlace | Open place | Открыть место | Joyni ochish |
| chest.progress | %{done} / %{required} · Check in at all %{required} places | %{done} / %{required} · Отметьтесь во всех %{required} местах | %{done} / %{required} · Barcha %{required} joyda belgilaning |
| weather.credit | Weather data by Open-Meteo.com | Погода: Open-Meteo.com | Ob-havo: Open-Meteo.com |
| empty.title | No places match your level and interests this month | Этот месяц нет мест под ваш уровень и интересы | Bu oy darajangiz va qiziqishlaringizga mos joy yo'q |
| empty.cta | Explore the map | Открыть карту | Xaritani ochish |
| info.title | How the path is built | Как строится путь | Yo'l qanday tuziladi |
| info.body | Every month we pick 3 places for your level and interests, best for the season and closest to Tashkent. Rings show this weekend's conditions. Check in at all 3 to open the chest. | Каждый месяц мы выбираем 3 места под ваш уровень и интересы — лучшие в этот сезон и ближе к Ташкенту. Кольца показывают условия на выходные. Отметьтесь во всех трёх, чтобы открыть сундук. | Har oy darajangiz va qiziqishlaringizga mos, mavsumga eng yaxshi va Toshkentga yaqin 3 ta joy tanlaymiz. Halqalar shu dam olish kunlari sharoitini ko'rsatadi. Sandiqni ochish uchun uchala joyda belgilaning. |
| seasons.winter/spring/summer/autumn | winter / spring / summer / autumn | зима / весна / лето / осень | qish / bahor / yoz / kuz |
| months.1..12 | January … December | Январь … Декабрь | Yanvar … Dekabr |
| monthsIn.1..12 (used by `status.opens` only) | January … December | в январе … в декабре | yanvar … dekabr |

ru `status.opens` = "Откроется %{month}" with `monthsIn` (→ "Откроется в мае"); en/uz use `monthsIn` too.

## testIDs · QA events
`path.screen` `path.node.<n>` `path.node.<n>.status` `path.popover.open-place` `path.chest` `path.info`
`path.weather` `path.empty` `path.retry` · `path_loaded { month, nodes, guest }` via `qaLog`

## Approved packages
none

## Done when
- [ ] Tests: renders 3 nodes + chest with the right chip per status. Guest request carries interests. Empty → Explore.
  Offline shows the cached path. Month change refetches.
- [ ] `npm run check` green, committed on the branch
