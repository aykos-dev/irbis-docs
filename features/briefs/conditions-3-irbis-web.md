# Brief conditions-3-irbis-web — admin Conditions page

- Spec: features/conditions.md · ACs in this slice: AC6
- Repo / branch: irbis-web · `feat/conditions` (create from main)
- Depends on: conditions-2-irbis-api (`openapi.json` on irbis-api `feat/conditions` → `npm run gen:api`)

## Files
- Touch: `src/features/conditions/` (new: `components/`, `hooks/`, `schemas.ts`, `__tests__/`) ·
  `src/app/(admin)/conditions/page.tsx` + `[placeId]/page.tsx` (or a side panel — follow users list → detail) ·
  `src/shared/components/layout/sidebar.tsx` (add item) · `src/shared/i18n/messages/{en,ru,uz}/conditions.json` (new)
- Read for patterns: `src/features/users/*` (list view, data-table, detail, action dialog, hooks over generated
  client), `src/shared/components/ui/*` (badge, confirm-dialog, data-table, field, empty/error states, skeleton),
  `design/design.md` § Condition status (in irbis-docs: chip bg/fg — Go #DFF6E7/#1B6B3E, Caution #FFF1BF/#6E4E00,
  Not now #FFE1E1/#B32424, Seasonal lock #ECEEEF/#56646A; icons check / warning triangle / circled × / lock)

## Behaviour (AC6)
- Sidebar "Conditions" (admin layout already admin-only). List: columns Place (name uz), Type, Status chip
  (colour + icon + label; null → grey "No data"), Source, Updated (relative from `computedAt`; forecast age in
  tooltip/sub-line), Flags (Closure / Override badges). Status filter: All, Go, Caution, Not now, Seasonal lock,
  No data (`none`) — in the URL query. Cursor "Load more". "Recompute now" → POST recompute; while pending or on
  409 RECOMPUTE_RUNNING: disabled + spinner + toast "Recompute already running"; success toast "Recompute started".
- Place view: status chip, reasons as plain codes→labels (en/ru/uz keys below), forecast time, closures table
  (start, end or "Open-ended", reason uz, source, Active/Ended) with "End" (confirm dialog), "Add closure" form:
  start (datetime-local, default now), end optional, reason uz required ≤ 280, ru/en optional ≤ 280, source
  Official/Admin. Override section: active override card + "End override" (confirm); form: status select, reason
  (same rules), expiry (datetime-local, default now + 3 days, max 14 days ahead, validated client-side with zod and
  server fieldErrors shown on fields). After any action, invalidate the place view + list queries.
- States: skeletons, empty ("No places for this filter"), error + retry, form errors, buttons disabled while submitting.
- Dates shown in Asia/Tashkent; sent as ISO UTC.

## API (generated hooks only)
`GET /v1/admin/conditions` · `GET /v1/admin/places/{id}/condition-controls` · `POST /v1/admin/places/{id}/closures` ·
`POST /v1/admin/closures/{id}/end` · `POST /v1/admin/places/{id}/overrides` · `POST /v1/admin/overrides/{id}/end` ·
`POST /v1/admin/conditions/recompute` — branch on `code`: CLOSURE_ALREADY_ENDED / OVERRIDE_ALREADY_ENDED → toast
"Already ended" + refetch; RECOMPUTE_RUNNING as above; VALIDATION_FAILED → field errors.

## Copy (namespace `conditions`)
| key | en | ru | uz |
|---|---|---|---|
| nav | Conditions | Условия | Holatlar |
| status.go / caution / not_now / seasonal_lock / none | Go / Caution / Not now / Seasonal lock / No data | Можно / Осторожно / Не сейчас / Закрыто на сезон / Нет данных | Borsa boʻladi / Ehtiyot boʻling / Hozir emas / Mavsumiy yopiq / Maʼlumot yoʻq |
| source.forecast / hazard_rule / closure / season / manual | Forecast / Hazard rule / Closure / Season / Manual override | Прогноз / Правило опасности / Закрытие / Сезон / Ручная установка | Prognoz / Xavf qoidasi / Yopilish / Mavsum / Qoʻlda belgilangan |
| recompute | Recompute now | Пересчитать | Qayta hisoblash |
| closures / addClosure / end / openEnded | Closures / Add closure / End / Open-ended | Закрытия / Добавить закрытие / Завершить / Без срока | Yopilishlar / Yopilish qoʻshish / Tugatish / Muddatsiz |
| override / setOverride / endOverride | Override / Set override / End override | Ручной статус / Установить / Снять | Qoʻlda holat / Oʻrnatish / Bekor qilish |
| field.start / end / expires / reasonUz / reasonRu / reasonEn / source / status | Starts / Ends / Expires / Reason (Uzbek) / Reason (Russian) / Reason (English) / Source / Status | Начало / Конец / Истекает / Причина (узб.) / Причина (рус.) / Причина (англ.) / Источник / Статус | Boshlanishi / Tugashi / Amal qilish muddati / Sabab (oʻzbekcha) / Sabab (ruscha) / Sabab (inglizcha) / Manba / Holat |
| sourceOfficial / sourceAdmin | Official / Admin | Официальное / Админ | Rasmiy / Admin |
| confirmEnd | End this now? The status updates at once. | Завершить сейчас? Статус обновится сразу. | Hozir tugatilsinmi? Holat darhol yangilanadi. |
| empty | No places for this filter | Нет мест по этому фильтру | Bu filtr boʻyicha joy yoʻq |
| updated | Updated {time} | Обновлено {time} | Yangilangan: {time} |

Reason code labels: reuse app wording without numbers — THUNDERSTORM Thunderstorm / Гроза / Momaqaldiroq; GUSTS Strong
gusts / Сильные порывы / Kuchli shamol esishi; HEAVY_PRECIP Heavy rain or snow / Сильные осадки / Kuchli yogʻin; WIND
Strong wind / Сильный ветер / Kuchli shamol; PRECIP_LIKELY Rain likely / Вероятны осадки / Yogʻin ehtimoli; HEAT Heat /
Жара / Issiq; COLD Severe cold / Сильный мороз / Qattiq sovuq; MUDSLIDE_RISK Mudslide risk / Риск селя / Sel xavfi;
FLOOD_RISK Flood risk / Риск паводка / Toshqin xavfi; AVALANCHE_RISK Avalanche risk / Лавинная опасность / Qor koʻchkisi
xavfi; GOOD_WEATHER Good weather / Хорошая погода / Ob-havo yaxshi; CLOSURE Closed / Закрыто / Yopiq; OVERRIDE Set by admin /
Установлено админом / Admin belgilagan.

## testIDs
`conditions-table`, `conditions-filter`, `conditions-recompute`, `conditions-row-<slug>`, `closure-form`, `override-form`

## Note from api (2e52ef3)
`PlaceListItem.conditionStatus` is optional (absent when a place has no condition yet) — treat absent like null.
Run `npm run gen:api` against irbis-api `feat/conditions` `openapi.json` (21 new schemas).

## Approved packages
none (native datetime-local inputs; no date picker package)

## Done when
- [ ] tests (list renders chips + filter; closure form validation; end confirm), `npm run check` green, committed
