# Brief places-3-irbis-app — Explore: map, list, filters, location

- Spec: features/places.md · ACs in this slice: AC4, AC5, AC6
- Repo / branch: irbis-app · `feat/places`
- Depends on: places-2-irbis-app (Place route, `placeTypes.ts`, `formatDistance.ts`, `places` i18n namespace)

## Files
- Touch: `src/features/places/screens/ExploreScreen.tsx`, `components/` (PlacesMap, PlaceCard, FilterChips,
  FilterSheet, LocationBanner), `hooks/useOrigin.ts` (permission + position), `exploreFilters.ts` (session store),
  `__tests__/` · `src/app/navigation/TabNavigator.tsx` (Explore → ExploreScreen; update the comment) ·
  `src/shared/constants/config.ts` (`mapStyleUrl` from react-native-config `MAP_STYLE_URL`, documented default in
  `.env.example` = `https://tiles.openfreemap.org/styles/liberty`) · `android/app/src/main/AndroidManifest.xml`
  (ACCESS_COARSE_LOCATION + ACCESS_FINE_LOCATION) · `ios/*/Info.plist` (NSLocationWhenInUseUsageDescription, en text)
  · `jest` setup mock for MapLibre (tests only) · `places.json` en/ru/uz (add keys below)
- Read for patterns (don't change): `src/shared/components/{Sheet,StatusChip,Pressable,EmptyState,ErrorState,
  OfflineBanner,Skeleton}.tsx`, `src/features/places/` from slice 2, `docs/architecture.md`; MapLibre RN docs via
  Context7 for the installed version (ShapeSource + cluster, CircleLayer/SymbolLayer, Camera, LocationManager)

## Behaviour
- AC4 — map fills the screen; one GeoJSON source from the list query (`limit=200`) with `cluster: true`; cluster
  circles show the count, tap a cluster → zoom in; single pins are type-coloured circles with the type glyph (colours
  from `placeTypes.ts`; waterfall/canyon placeholder colours there). Bottom sheet (collapsed ~40 %, drag to expand):
  header `explore.count` (plural) by `origin`, "Sorted by distance"; FlatList of PlaceCard (illustration thumb, name
  locale→uz, "{Type} · {distance}", boots) in API order; tap card or single pin → `Place { id, lat?, lng? }`.
  States: skeleton sheet while loading, ErrorState + retry, offline = cached list + OfflineBanner, else offline message.
- AC5 — chips row over the map: Type, Difficulty, Distance; each opens FilterSheet; "Show places" applies (one query
  key → map + list refetch together); active chip shows value: types joined " · " by plural label (more than 2 → first
  two + "+N"), "Difficulty {min}–{max}", "≤ {km} km"; Distance options 50 / 100 / 150 / Any (default Any).
  Filters held in a module/session store (survive tab switches and Place round-trip, reset on app restart).
  Zero items → EmptyState "No places match these filters" + "Reset filters" (clears all). Selection haptic on toggles.
  Back from Place keeps list scroll position.
- AC6 — `useOrigin`: on first Explore mount request location (MapLibre `requestAndroidLocationPermissions` / iOS
  when-in-use). Granted → get one fix (timeout 10 s) → pass `lat/lng` to the query, camera to user (zoom ~8). Denied /
  blocked / off / timeout → no coords (API answers `origin: 'tashkent'`), camera to Tashkent 41.2995, 69.2401 (zoom 7),
  LocationBanner with "Turn on": re-request if still requestable, else `Linking.openSettings()`. On AppState → active,
  re-check permission; newly granted → fetch fix and refetch with device origin. If MapLibre's location API can't do
  this, stop and report — do not add a geolocation package (needs approval).
- QA events: `location_permission { result }` (granted|denied|blocked|unavailable), `explore_loaded { count, origin }`
  per successful list load, `explore_filters_applied { types, difficultyMin, difficultyMax, maxKm, count }`.

## Copy (`places` namespace; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| explore.countDevice (plural) | {{count}} places near you | one: {{count}} место рядом с вами · few: {{count}} места рядом с вами · many: {{count}} мест рядом с вами | Yaqiningizda {{count}} ta joy |
| explore.countTashkent (plural) | {{count}} places from Tashkent | one: {{count}} место от Ташкента · few: {{count}} места от Ташкента · many: {{count}} мест от Ташкента | Toshkentdan {{count}} ta joy |
| explore.sorted | Sorted by distance | По расстоянию | Masofa bo‘yicha |
| explore.cardMeta | {{type}} · {{distance}} | {{type}} · {{distance}} | {{type}} · {{distance}} |
| typePlural.peak … canyon | Peaks · Lakes · Caves · Camping · Trails · Waterfalls · Canyons | Пики · Озёра · Пещеры · Кемпинги · Тропы · Водопады · Каньоны | Cho‘qqilar · Ko‘llar · G‘orlar · Lagerlar · So‘qmoqlar · Sharsharalar · Kanyonlar |
| filter.type / difficulty / distance | Type / Difficulty / Distance | Тип / Сложность / Расстояние | Turi / Qiyinlik / Masofa |
| filter.difficultyRange | Difficulty {{min}}–{{max}} | Сложность {{min}}–{{max}} | Qiyinlik {{min}}–{{max}} |
| filter.maxKm / filter.any | ≤ {{km}} km / Any | ≤ {{km}} км / Любое | ≤ {{km}} km / Istalgan |
| filter.apply / filter.reset | Show places / Reset filters | Показать места / Сбросить фильтры | Joylarni ko‘rsatish / Filtrlarni tozalash |
| explore.empty | No places match these filters | Нет мест по этим фильтрам | Bu filtrlarga mos joy yo‘q |
| location.banner / location.turnOn | Turn on location to see distances from you / Turn on | Включите геолокацию, чтобы видеть расстояние от вас / Включить | Sizdan masofani ko‘rish uchun joylashuvni yoqing / Yoqish |

## testIDs
`explore.screen`, `explore.map`, `explore.sheet`, `explore.count`, `explore.card.<slug>`, `explore.filter.type`,
`explore.filter.difficulty`, `explore.filter.distance`, `explore.filter.apply`, `explore.filter.reset`,
`explore.empty`, `explore.location-banner`, `explore.location-turn-on`

## Approved packages
`@maplibre/maplibre-react-native` — latest stable compatible with RN 0.88 New Arch (owner Q2). Nothing else.

## Done when
- [ ] tests: count header by origin, filter → query params + chip labels, empty + reset, denied → banner + no coords
- [ ] `npm run check` green; Android debug build compiles (`cd android && ./gradlew assembleDebug -q | tail -30`)
- [ ] committed on `feat/places`; reply ≤ 10 lines (package version added, anything open)
