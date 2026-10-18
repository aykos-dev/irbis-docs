# Brief conditions-4-irbis-app — Place condition card, weather, hazards now, Explore chips

- Spec: features/conditions.md · ACs in this slice: AC7, AC8
- Repo / branch: irbis-app · `feat/conditions` (create from main)
- Depends on: conditions-2-irbis-api (`openapi.json` on irbis-api `feat/conditions` → `npm run gen:api`)

## Files
- Touch: `src/features/conditions/` (new: `components/ConditionCard.tsx`, `WeatherCard.tsx`, `HazardsNow.tsx`,
  `hooks/usePlaceCondition.ts`, `reasonText.ts` (pure), `weatherGlyph.tsx` (placeholder glyphs), `__tests__/`) ·
  `src/features/places/screens/PlaceScreen.tsx` (mount card under the level card; weather; swap hazards list for
  HazardsNow when hazards levels exist) · `src/features/places/components/PlaceCard.tsx` (status chip) ·
  `src/shared/i18n/{en,ru,uz}/conditions.json` (new) — places importing a conditions component: move the
  three components to `src/shared/components/conditions/` instead if boundaries forbid feature→feature imports
- Read for patterns: `src/shared/components/StatusChip.tsx` (use it: variants go/caution/notNow/seasonalLock),
  `IrbisMascot.tsx` / `Mascot.tsx` (worried pose `9dde5ea7…` — check which asset exists; if missing, copy the canvas
  SVG via design/assets.md id), `src/features/places/components/LevelCard.tsx`, `SeasonBar.tsx`, `hooks/usePlace.ts`,
  `ErrorState`, `Skeleton`, `OfflineBanner`

## Behaviour
- AC7 — `usePlaceCondition(id)` (generated hook). Card (`place.condition`): StatusChip + title; `status` null →
  grey card "Condition not available yet" (`place.condition-empty`). Sub-line "Updated {relative} · {source}" from
  `computedAt` (relative: "just now" < 1 min, "{n} min ago", "{n} h ago", "{n} d ago"). Up to 3 reason lines
  (`place.condition-reason.<n>`) from `reasonText(reason, locale)`; source closure/manual → admin `text[locale] ??
  text.uz` as the single line. Not now → worried Irbis (small, right). Seasonal lock title uses `opensMonth`
  (full month name in locale; null → "Closed for the season"). Weather card (`place.weather`) only when `weekend`
  non-empty: one row per day (`place.weather-day.sat|sun`): glyph by `weatherCode` (0–1 sun, 2–3 cloud, 45–48 cloud,
  51–67/80–82 rain, 71–77/85–86 snow, 95–99 storm), "{Day} {max}° / {min}°"; then "Wind {kmh} km/h · Rain {pct}%"
  (max over days); footer "Weather data by Open-Meteo.com". Hazards now: each `hazards[]` item
  (`place.hazard.<hazard>`) label + level; empty array → existing "Hazards not set yet". Light + dark.
- AC8 — `PlaceCard` shows StatusChip (`explore.card.<slug>.status`) next to "{Type} · {distance}" when
  `conditionStatus` non-null. Offline: React Query cache shows last data with its "Updated" age; no cache → card
  offline message + "Try again" (`place.condition-retry`). Fetch error → `place.condition-error` + retry; the rest
  of Place renders. QA events: `condition_viewed { slug, status, source, ageMin }` once per open;
  `explore_loaded` adds `withStatus`.

## Copy (namespace `conditions`; `{day}` = Saturday/Sunday in locale)
| key | en | ru | uz |
|---|---|---|---|
| status.go/caution/not_now/seasonal_lock | Go / Caution / Not now / Seasonal lock | Можно / Осторожно / Не сейчас / Закрыто на сезон | Borsa boʻladi / Ehtiyot boʻling / Hozir emas / Mavsumiy yopiq |
| title.go/caution/not_now | Go this weekend / Caution this weekend / Not now this weekend | Можно в эти выходные / Осторожно в эти выходные / Не в эти выходные | Bu dam olish kunlari borsa boʻladi / Bu dam olishda ehtiyot boʻling / Bu dam olishda hozir emas |
| title.seasonal / seasonalOpens | Closed for the season / Closed for the season · Opens in {month} | Закрыто на сезон / Закрыто на сезон · Откроется в {month} | Mavsum uchun yopiq / Mavsum uchun yopiq · {month} oyida ochiladi |
| empty | Condition not available yet | Состояние пока недоступно | Holat hozircha mavjud emas |
| updated | Updated {time} · {source} | Обновлено {time} · {source} | Yangilangan: {time} · {source} |
| source.forecast/hazard_rule/closure/season/manual | forecast / hazard rules / closure / season / Irbis team | прогноз / правила опасности / закрытие / сезон / команда Irbis | prognoz / xavf qoidalari / yopilish / mavsum / Irbis jamoasi |
| reason.THUNDERSTORM | Thunderstorm on {day} | Гроза в {day} | {day} kuni momaqaldiroq |
| reason.GUSTS | Gusts up to {value} km/h on {day} | Порывы до {value} км/ч в {day} | {day} kuni shamol {value} km/soatgacha esadi |
| reason.HEAVY_PRECIP | Heavy rain or snow on {day} — {value} mm | Сильные осадки в {day} — {value} мм | {day} kuni kuchli yogʻin — {value} mm |
| reason.WIND | Strong wind on {day} — {value} km/h | Сильный ветер в {day} — {value} км/ч | {day} kuni kuchli shamol — {value} km/soat |
| reason.PRECIP_LIKELY | Rain likely on {day} — {value}% | Вероятны осадки в {day} — {value}% | {day} kuni yogʻin ehtimoli — {value}% |
| reason.HEAT | Heat on {day} — up to {value}° | Жара в {day} — до {value}° | {day} kuni issiq — {value}° gacha |
| reason.COLD | Severe cold on {day} — down to {value}° | Сильный мороз в {day} — до {value}° | {day} kuni qattiq sovuq — {value}° gacha |
| reason.MUDSLIDE_RISK / FLOOD_RISK | Mudslide risk after rain on {day} / Flood risk after rain on {day} | Риск селя после дождя в {day} / Риск паводка после дождя в {day} | {day} kuni yomgʻirdan keyin sel xavfi / toshqin xavfi |
| reason.AVALANCHE_RISK | Avalanche risk — {value} cm of fresh snow | Лавинная опасность — {value} см свежего снега | Qor koʻchkisi xavfi — {value} sm yangi qor |
| reason.GOOD_WEATHER | Good weather on {day}, wind up to {value} km/h | Хорошая погода в {day}, ветер до {value} км/ч | {day} kuni ob-havo yaxshi, shamol {value} km/soatgacha |
| day.sat / day.sun | Saturday / Sunday | субботу / воскресенье | Shanba / Yakshanba |
| weather.title / wind / rain / credit | Weather this weekend / Wind {kmh} km/h / Rain {pct}% / Weather data by Open-Meteo.com | Погода на выходные / Ветер {kmh} км/ч / Осадки {pct}% / Данные о погоде: Open-Meteo.com | Dam olish kunlari ob-havosi / Shamol {kmh} km/soat / Yogʻin {pct}% / Ob-havo maʼlumotlari: Open-Meteo.com |
| hazards.title / level.low/raised/high/open/closed | Hazards now / Low / Raised / High / Open / Closed | Опасности сейчас / Низкая / Повышенная / Высокая / Открыта / Закрыта | Hozirgi xavflar / Past / Oshgan / Yuqori / Ochiq / Yopiq |
| offline / error / retry | You're offline — condition not loaded / Couldn't load the condition / Try again | Нет сети — состояние не загружено / Не удалось загрузить состояние / Повторить | Internet yoʻq — holat yuklanmadi / Holatni yuklab boʻlmadi / Qayta urinish |
Weather-row day labels use nominative: Sat/Sun → ru "Сб"/"Вс", uz "Sha"/"Yak", en "Sat"/"Sun" (`dayShort.*`).

## Approved packages
none · weather glyphs are simple react-native-svg placeholders (owner art later)

## Done when
- [ ] tests: reasonText per code + locale fallback; ConditionCard null/not_now/seasonal states; PlaceCard chip;
  `npm run check` green, committed on `feat/conditions`
